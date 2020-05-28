# twitter-data-extraction
## Descrição
Scripts para coleta/extração de tweets usando __Python 3.7.7__ e a Standard API do Twitter.

## Pré-requisitos
Além de possuir uma conta de usuário no [Twitter](https://twitter.com/explore), você também deve ter uma conta de desenvolvedor, que pode ser obtida no [Twitter Developer](https://developer.twitter.com/en), com um app registrado para a criação dos tokens de acesso.

Uma vez que você já possua esses tokens, use o arquivo `tokens.json` mostrado abaixo para realizar a configuração inicial dos scripts de extração de tweets:

```json
{
    "access_token" : "your_access_token",
    "access_token_secret" : "your_access_token_secret",
    "api_key" : "your_api_key",
    "api_secret_key" : "your_api_secret_key"
}
```

## Bibliotecas utlizadas
* [tweepy](http://docs.tweepy.org/en/latest/)
* [numpy](https://numpy.org/)
* [pandas](https://pandas.pydata.org/)
* [prettytable](https://ptable.readthedocs.io/en/latest/index.html)

## Exemplos de uso
Informações gerais sobre o funcionamento dos scripts podem ser visualizadas utilizando os comandos:

~~~
python get_tweets.py -h
~~~
~~~
python get_user_tweets.py -h
~~~
~~~
python get_liked_tweets.py -h
~~~

#### get_tweets.py
Para coletar tweets com o termo de busca __coronavirus__, tendo como arquivo de saída __coronavirus_tweets__, execute o comando:
~~~
python get_tweets.py coronavirus coronavirus_tweets
~~~

É possível também fazer a coleta de tweets usando uma lista de termos, que devem estar entres aspas (simples ou duplas):
~~~
python get_tweets.py 'coronavirus,covid-19,coronga' coronavirus_tweets
~~~

Para coletar tweets em um idioma em específico:
~~~
python get_tweets.py --lang en coronavirus coronavirus_tweets
~~~

#### get_user_tweets.py
Para coletar tweets de um perfil em específico:
~~~
python get_users_tweets.py --username @folha
~~~
No exemplo anterior, o arquivo gerado contém o nome do perfil (folha.txt, por exemplo). Caso queira um nome diferente para o arquivo de saída, use o comando:
~~~
python get_users_tweets.py --username @folha --output folha_tweets
~~~
A coleção de tweets obtidas consiste naqueles escritos pelo perfil, suas replies à outras postagens e retweets. Caso deseje excluir replies e/ou retweets:
~~~
python get_users_tweets.py --username @folha --exclude_rts --exclude_replies
~~~
A coleta dos tweets pode ser feita em dois modos:
1. __default__: é feita somente uma requisição para a API. É o modo padrão de coleta dos scripts. Coleta até 100 tweets para `get_tweets.py` e até 200 tweets para `get_users_tweets.py`.
2. __extended__: executa várias requisições até que seja atingido o Rate Limit da API. Dessa forma, este modo permite uma coleta mais vasta de tweets.
~~~
python get_tweets.py --lang en coronavirus coronavirus_tweets --mode extended
~~~
~~~
python get_users_tweets.py --username @folha --mode extended
~~~

#### get_liked_tweets.py
Para buscar os últimos tweets curtidos pelo perfil [@legadaodamassa](https://twitter.com/legadaodamassa), por exemplo:
~~~
get_liked_tweets.py --username @legadaodamassa
~~~
Por padrão, o script busca as últimas 200 curtidas. Para alterar esse valor:
~~~
get_liked_tweets.py --username @legadaodamassa --count 1000
~~~
No terminal, ao fim da execução do script, será mostrado um ranking com os perfis mais curtidos, com 10 posições por padrão. Para alterar esse número de posições:
~~~
get_liked_tweets.py --username @legadaodamassa --count 1000 --ranking 15
~~~
Por definição, após a execução dos comendos listados anteriormente, o script sempre criará dois arquivos:
1. arquivo __json__, contendo a resposta completa da API para as requisições, nomeado com o valor fornecido para o argumento `--username`. Para alterar o nome desse arquivo:
 ~~~
 get_liked_tweets.py --username @legadaodamassa --output_file likes_do_legadao
 ~~~
2. arquivo __txt__ contendo o ranking completo de todos os perfis curtidos, presentes na resposta da API, nomeado como `likes_ranking.txt`. Para alterar o nome desse arquivo:
 ~~~
 get_liked_tweets.py --username @legadaodamassa --ranking_file ranking_legadao
 ~~~
Há ainda a possibilidade de, caso já tenha um arquivo json com a resposta da API pela busca de curtidas, fornecer o arquivo como parametro de entrada para o script, como por exemplo:
~~~
python get_liked_tweets.py --input_file likes_do_legadao.json --ranking 20 --ranking_file top_likes_legadao
~~~

## Licença
Copyright 2020 Geandreson Costa.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.