# Pipeline de Dados com o Airflow para Baixar Podcasts
Neste projeto, iremos construir um pipeline de dados com quatro etapas usando o Airflow, que é uma ferramenta popular de engenharia de dados baseada em Python para definir e executar pipelines de dados muito poderosos e flexíveis. O pipeline irá baixar episódios de podcast. Armazenaremos nossos resultados em um banco de dados SQLite que pode ser facilmente consultado. 

## Bibliotecas Necessárias:
- os: Para operações relacionadas a arquivos e pastas.
- json: Para trabalhar com JSON.
- requests: Para fazer solicitações HTTP ao feed de podcast.
- xmltodict: Para analisar o XML do feed de podcast.
- pendulum: Para manipulação de datas e horários.
- airflow.decorators: Para criar tarefas no Apache Airflow.
- airflow.providers.sqlite.operators.sqlite: Para operações SQLite no Airflow.
- airflow.providers.sqlite.hooks.sqlite: Para conectar ao banco de dados SQLite no Airflow.
- vosk: Para reconhecimento de fala.
- pydub: Para processamento de áudio.

## Variáveis Globais:
- PODCAST_URL: URL do feed de podcast a ser analisado.
- EPISODE_FOLDER: Pasta onde os episódios de áudio serão armazenados.
- FRAME_RATE: Taxa de quadros para o áudio.

## Funções e Tarefas:
1. 'create_table_sqlite': Tarefa que cria uma tabela SQLite para armazenar informações sobre os episódios.

2. 'get_episodes': Tarefa para obter os episódios do feed de podcast. Faz uma solicitação HTTP ao PODCAST_URL e analisa o XML para recuperar os episódios.

3. 'load_episodes': Tarefa para carregar episódios novos que não estão na tabela SQLite. Compara os episódios obtidos com os já armazenados e seleciona os novos para serem adicionados à tabela.

4. 'download_episode': Tarefa para baixar um episódio de áudio. Verifica se o episódio já foi baixado e, se não, faz o download e salva em EPISODE_FOLDER.

5. 'transcribe_episode': Tarefa para transcrever um episódio de áudio. Utiliza o modelo de reconhecimento de fala Vosk para transcrever o áudio e atualiza a tabela SQLite com a transcrição.

6. O DAG executa as tarefas na seguinte ordem:
   - Criação da tabela SQLite.
   - Obtenção dos episódios do feed de podcast.
   - Carregamento de episódios novos.
   - Download e transcrição de episódios não baixados ou transcritos.

7. Cada tarefa é uma unidade de processamento independente que pode ser agendada e executada pelo Apache Airflow. O DAG orquestra a sequência de execução das tarefas.

## Exemplo de Uso:
- Crie uma instância do DAG 'podcast_summary' usando a variável 'summary'. O DAG pode ser agendado e executado pelo Apache Airflow.

## Observações:
- É importante configurar as dependências, como o banco de dados SQLite e o modelo Vosk, antes de executar o DAG.

