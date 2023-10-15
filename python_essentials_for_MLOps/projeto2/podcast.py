"""
Build an Airflow Data Pipeline to Download Podcasts
Editado por: Elisa Gabriela Machado de Lucena
"""
# Importações de bibliotecas necessárias
import logging
import os
import json
import requests
import xmltodict
import pendulum
from airflow.decorators import dag, task
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.sqlite.hooks.sqlite import SqliteHook
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

# Configurando o logging
logging.basicConfig(filename='podcast.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# URL do feed de podcast a ser analisado
PODCAST_URL = "https://www.marketplace.org/feed/podcast/marketplace/"

# Pasta onde os episódios de áudio serão armazenados
EPISODE_FOLDER = "episodes"

# Taxa de quadros para o áudio
FRAME_RATE = 16000

@dag(
    dag_id='podcast_summary',
    schedule_interval="@daily",
    start_date=pendulum.datetime(2022, 5, 30),
    catchup=False,
)
def podcast_summary():
    """
    Cria um DAG (Directed Acyclic Graph) do Airflow chamado 'podcast_summary' para analisar um feed de podcast.
    """

    create_database = SqliteOperator(
        task_id='create_table_sqlite',
        sql=r"""
        CREATE TABLE IF NOT EXISTS episodes (
            link TEXT PRIMARY KEY,
            title TEXT,
            filename TEXT,
            published TEXT,
            description TEXT,
            transcript TEXT
        );
        """,
        sqlite_conn_id="podcasts"
    )

    @task()
    def get_episodes():
        """
        Obtém os episódios do feed de podcast.
        """
        data = requests.get(PODCAST_URL, timeout=10)  # Adicionado timeout
        feed = xmltodict.parse(data.text)
        episodes = feed["rss"]["channel"]["item"]
        print(f"Found {len(episodes)} episodes.")
        return episodes

    @task()
    def load_episodes(episodes, stored_episodes):
        """
        Carrega episódios novos que não estão na tabela SQLite.
        """
        new_episodes = []
        for episode in episodes:
            if episode["link"] not in stored_episodes["link"].values:
                filename = f"{episode['link'].split('/')[-1]}.mp3"
                new_episodes.append([episode["link"], episode["title"], episode["pubDate"], episode["description"], filename])
        return new_episodes

    @task()
    def download_episode(episode):
        """
        Baixa um episódio de áudio.
        """
        name_end = episode["link"].split('/')[-1]
        filename = f"{name_end}.mp3"
        audio_path = os.path.join(EPISODE_FOLDER, filename)
        if not os.path.exists(audio_path):
            print(f"Downloading {filename}")
            audio = requests.get(episode["enclosure"]["@url"], timeout=10)  # Adicionado timeout
            with open(audio_path, "wb+") as f:
                f.write(audio.content)
        return {"link": episode["link"], "filename": filename}

    @task()
    def transcribe_episode(episode, frame_rate=FRAME_RATE):  # Alterado argumento para frame_rate
        """
        Transcreve um episódio de áudio.
        """
        hook = SqliteHook(sqlite_conn_id="podcasts")
        print(f"Transcribing {episode['filename']}")
        filepath = os.path.join(EPISODE_FOLDER, episode["filename"])
        mp3 = AudioSegment.from_mp3(filepath)
        mp3 = mp3.set_channels(1)
        mp3 = mp3.set_frame_rate(frame_rate)  # Usando o argumento frame_rate

        model = Model(model_name="vosk-model-en-us-0.22-lgraph")
        rec = KaldiRecognizer(model, frame_rate)  # Usando o argumento frame_rate
        rec.SetWords(True)

        step = 20000
        transcript = ""
        for i in range(0, len(mp3), step):
            print(f"Progress: {i/len(mp3)}")
            segment = mp3[i:i+step]
            rec.AcceptWaveform(segment.raw_data)
            result = rec.Result()
            text = json.loads(result)["text"]
            transcript += text

        hook.insert_rows(table='episodes', rows=[[episode["link"], transcript]], target_fields=["link", "transcript"], replace=True)

    podcast_episodes = get_episodes()
    stored_episodes = load_episodes(podcast_episodes, podcast_episodes)
    new_episodes = load_episodes(podcast_episodes, stored_episodes)

    download_tasks = []
    transcribe_tasks = []

    for episode in new_episodes:
        download_task = download_episode(episode)
        download_tasks.append(download_task)
        transcribe_task = transcribe_episode(download_task, FRAME_RATE)  # Passando FRAME_RATE como argumento
        transcribe_tasks.append(transcribe_task)

    return {
        'create_database': create_database,
        'get_episodes': podcast_episodes,
        'download_episodes': download_tasks,
        'transcribe_episodes': transcribe_tasks
    }

if __name__ == '__main__':
    summary = podcast_summary()
    
