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

~~~
python get_tweets.py coronavirus coronavirus_tweets
~~~

~~~
python get_tweets.py --lang en coronavirus coronavirus_tweets
~~~

~~~
python get_tweets.py --lang en coronavirus coronavirus_tweets --mode extended
~~~
