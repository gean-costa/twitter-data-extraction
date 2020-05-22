# twitter-data-extraction
### Descrição
Scripts para coleta/extração de tweets usando __Python 3.7.7__ e a Standard API do Twitter.

### Pré-requisitos
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

### Bibliotecas utlizadas
* [tweepy](http://docs.tweepy.org/en/latest/)

### Exemplos de uso
Informações gerais sobre o funcionamento do script podem ser visualizadas utilizando o comando:

~~~
python get_tweets.py -h
~~~

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

A coleta dos tweets pode ser feita em dois modos:
1. __default__: coleta somente 100 tweets, padrão da API, pois é feita somente uma requisição para ela. É o modo padrão de coleta de tweets do script.
2. __extended__: executa várias requisições, coletando 100 tweets cada, até que seja atingido o Rate Limit da API. Dessa forma, este modo permite uma coleta mais vasta de tweets.
~~~
python get_tweets.py --lang en coronavirus coronavirus_tweets --mode extended
~~~
