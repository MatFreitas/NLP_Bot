## Como foi o plano? 

Para realizar essa APS, peguei o modelo que realizamos em aula para fazer o classificador de sentimento. No caso, tratava-se de um clasificador
Naive Bayes que utilizava como base de dados as críticas de filmes do IMDB, contendo 50 mil valores. Salvei esse modelo com o joblib e apliquei
no meu projeto. Depois, aumentei a query search para retornar mais de um resultado de pesquisa (para três agora), de tal forma que se uma página
ficasse abaixo do filtro estabelecido, o código procura a segunda opção mais relevante, e assim por diante.

## Que dificuldades foram encontradas?

Tive dificuldade apenas em tratar os novos comandos. Antes, bastava dizer apenas que depois da palavra 'search'/'wn_search', tudo o que vinha depois
eram palavras da query. No entanto, agora que existe a possibilidade do filtro th, tive que tratar o comando, ficou um pouco hard-coded mas funciona.

## Quais foram as fontes consultadas?

Aulas do curso.

## Interações com o GPT

N/A