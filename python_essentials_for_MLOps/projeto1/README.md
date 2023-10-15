# Sistema de recomendação de filmes
Neste projeto, iremos construir um sistema interativo de recomendação de filmes que permite que você digite o nome de um filme e imediatamente obtenha dez recomendações de outros filmes que você pode querer assistir. 
O sistema utiliza técnicas de Processamento de Linguagem Natural (NLP) para calcular a similaridade entre os títulos dos filmes. Ele também leva em consideração as classificações dos usuários para fornecer recomendações personalizadas.

## Descrição do Projeto
O sistema é composto por várias partes:

* Pré-processamento de Dados: Os dados dos filmes são carregados a partir de arquivos CSV. Os títulos dos filmes são limpos para remover caracteres extras.

* Pesquisa de Filmes: Os usuários podem inserir um termo de pesquisa para encontrar filmes com títulos semelhantes. Isso é útil quando eles desejam descobrir novos filmes com base em suas preferências.

* Recomendação com Base no Filme de Referência: Os usuários podem fornecer o ID de um filme que gostam, e o sistema encontrará filmes semelhantes com base nas classificações de outros usuários. Isso é útil para descobrir filmes relacionados a um filme específico.

## Instruções de Uso
Para usar o sistema de recomendação de filmes, siga estas etapas:

Certifique-se de que você tem os seguintes arquivos no mesmo diretório do código:

movies.csv (contendo informações sobre os filmes)
ratings.csv (contendo informações sobre as classificações dos usuários)
Execute o código em um ambiente Python compatível. Você pode usar o Jupyter Notebook ou qualquer IDE Python de sua escolha.

Você verá duas caixas de texto interativas: "Movie Title" e "Movie Title" (novamente).

No primeiro, insira o título do filme que deseja pesquisar e pressione "Enter" para obter recomendações com base no termo de pesquisa.
No segundo, insira o título de um filme que você gosta e pressione "Enter" para obter recomendações com base nesse filme.
As recomendações de filmes serão exibidas abaixo das caixas de texto.

## Instalação
Para executar o código, você precisará das seguintes bibliotecas Python instaladas:

* pandas
* numpy
* ipywidgets
* scikit-learn (sklearn)
  
Você pode instalá-los usando o pip, caso ainda não estejam instalados:
```
pip install pandas numpy ipywidgets scikit-learn
```
Além disso, certifique-se de que os arquivos "movies.csv" e "ratings.csv" estejam no mesmo diretório em que o código está localizado.
