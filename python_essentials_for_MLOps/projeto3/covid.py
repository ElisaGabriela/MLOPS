"""
Analyzing COVID RNA Sequences in Python
editado por: Elisa Gabriela Machado de Lucena
"""
import logging
import io
import pandas as pd
from Bio import Entrez
from Bio import SeqIO
from Bio import Align
import numpy as np
from IPython.display import HTML
from IPython.display import display

# Configurando o logging
logging.basicConfig(filename='covid.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Função para fazer o download de sequências
def download_sequence(id_code):
    """
    Faz o download de uma sequência a partir de um ID de acesso.

    Args:
        id_code (str): O ID de acesso da sequência.

    Returns:
        str: A sequência no formato FASTA.
    """
    handle = Entrez.esearch(db="nucleotide", term=id_code, retmax="1")
    record = Entrez.read(handle)
    handle = Entrez.efetch(db="nucleotide", id=record["IdList"][0], rettype="fasta", retmode="text")
    return handle.read()

# Função para colorir o texto em HTML
def color_print(s, color='black'):
    """
    Retorna o texto colorido em HTML.

    Args:
        s (str): O texto a ser colorido.
        color (str): A cor desejada.

    Returns:
        str: O texto colorido em HTML.
    """
    return "<span style='color:{}'>{}</span>".format(color, s)

# Leitura do arquivo CSV
metadata = pd.read_csv("ncbi_datasets.csv")

# Pré-processamento dos dados
metadata["Collection Date"] = pd.to_datetime(metadata["Collection Date"])
metadata.columns = [c.lower().replace(" ", "_") for c in metadata.columns]
metadata["continent"] = metadata["geo_location"].str.replace(";.+", "", regex=True)
metadata.groupby("continent").apply(lambda x: x.sort_values("collection_date").iloc[0])
sample_month = pd.Series(metadata["collection_date"].values.astype("<M8[M]"))

# Sequências de referência e variantes
sequences = ["NC_045512.2", "OL467832.1", "OM061695.1",  "OM095411.1"]
human_names = ["reference", "base", "delta", "omicron"]

# Seleção das sequências no metadata
selected_sequences = metadata[metadata["nucleotide_accession"].isin(sequences)]

# Configuração do e-mail para Entrez
Entrez.email = "vik@dataquest.io"

# Download das sequências
sequence_data = {}
for sequence in sequences:
    sequence_data[sequence] = {"fasta": download_sequence(sequence)}

# Parse das sequências no formato FASTA
for k, v in sequence_data.items():
    f = io.StringIO(v["fasta"])
    sequence_data[k]["parsed"] = list(SeqIO.parse(f, "fasta"))[0]

# Configuração do alinhador
aligner = Align.PairwiseAligner()

# Cálculo do score de alinhamento entre duas sequências
score = aligner.score(sequence_data["NC_045512.2"]["parsed"].seq, sequence_data["OM061695.1"]["parsed"].seq)

# Criação de uma matriz de comparações
comparisons = np.zeros((4, 4))

for i in range(0, 4):
    for j in range(0, i + 1):
        score = aligner.score(sequence_data[sequences[i]]["parsed"].seq, sequence_data[sequences[j]]["parsed"].seq)
        comparisons[i, j] = score

# Criação de um DataFrame para as comparações
comparison_df = pd.DataFrame(comparisons, columns=human_names, index=human_names)

# Alinhamento de duas sequências
seq1 = sequence_data["NC_045512.2"]["parsed"].seq
seq2 = sequence_data["OM061695.1"]["parsed"].seq
delta_alignments = aligner.align(seq1, seq2)

# Seleção do primeiro alinhamento
delta_alignment = delta_alignments[0]

# Identificação e exibição de regiões não alinhadas
SEQ1_END = None
SEQ2_END = None
for alignments in zip(delta_alignment.aligned[0], delta_alignment.aligned[1]):

    if SEQ1_END and SEQ2_END:
        seq1_mismatch = seq1[SEQ1_END:alignments[0][0]]
        seq2_mismatch = seq2[SEQ2_END:alignments[1][0]]
        print("1: {}".format(seq1_mismatch))
        print("2: {}".format(seq2_mismatch))

    SEQ1_END = alignments[0][1]
    SEQ2_END = alignments[1][1]

# Exibição das sequências com formatação HTML para destacar regiões de diferença
SEQ1_END = None
SEQ2_END = None
display_seq = []
for alignments in zip(delta_alignment.aligned[0], delta_alignment.aligned[1]):

    if SEQ1_END and SEQ2_END:
        seq1_mismatch = seq1[SEQ1_END:alignments[0][0]]
        seq2_mismatch = seq2[SEQ2_END:alignments[1][0]]
        if len(seq2_mismatch) == 0:
            display_seq.append(color_print(seq1[SEQ1_END:alignments[0][0]], "red"))
        elif len(seq1_mismatch) == 0:
            display_seq.append(color_print(seq2[SEQ2_END:alignments[1][0]], "green"))
        else:
            display_seq.append(color_print(seq2[SEQ2_END:alignments[1][0]], "blue"))

    display_seq.append(seq1[alignments[0][0]:alignments[0][1]])

    SEQ1_END = alignments[0][1]
    SEQ2_END = alignments[1][1]

# Conversão das sequências em uma lista de strings
display_seq = [str(i) for i in display_seq]

# Exibição das sequências formatadas em HTML
display(HTML('<br>'.join(display_seq)))
