# Analisando a sequência RNA do COVID em Python
Neste projeto, vamos baixar e analisar os dados das sequências de RNA do COVID em duas de suas principais variantes: Delta e Ômicron. O RNA é um ácido nucleico presente em todas as células vivas e é composto por uma única fita que consiste em várias combinações 
de quatro nucleotídeos: uracila, citosina, adenina e guanina. O RNA é o "código-fonte" do COVID que permite ao vírus entrar na célula e se replicar.

## Divisão do Algoritmo

O código está dividido em várias partes para facilitar a compreensão:

1. **Download de Sequências**: Baixa sequências de RNA a partir de IDs de acesso usando a biblioteca Biopython.

2. **Pré-processamento de Dados**: Realiza o pré-processamento dos dados, formatando datas e renomeando colunas.

3. **Seleção de Sequências**: Seleciona sequências específicas com base em critérios, como o nome da variante do COVID-19.

4. **Alinhamento de Sequências**: Utiliza uma biblioteca de alinhamento para comparar as sequências selecionadas.

5. **Exibição de Resultados**: Os resultados são formatados em HTML para destacar regiões de diferença entre as sequências e, em seguida, são exibidos.

## Instruções de Uso

Para usar o código, siga estas instruções:

1. **Configuração do Ambiente**:
   - Certifique-se de que você tem Python instalado.
   - Instale as bibliotecas necessárias executando o seguinte comando:
     ```
     pip install biopython pandas numpy
     ```

2. **Executando o Código**:
   - Execute o código em um ambiente Python. Certifique-se de estar no diretório onde o código está localizado e execute-o.

3. **Visualização dos Resultados**:
   - Os resultados são exibidos em HTML. Você pode visualizá-los em um navegador ou em um ambiente Python com suporte a HTML.

## Instruções de Instalação

Se você ainda não possui as dependências necessárias, siga estas instruções para instalá-las:

1. **Python**: Se você não possui o Python instalado, faça o download e instale a partir do [site oficial do Python](https://www.python.org/).

2. **Bibliotecas**:
   - Instale as bibliotecas necessárias executando o seguinte comando:
     ```
     pip install biopython pandas numpy
     ```
