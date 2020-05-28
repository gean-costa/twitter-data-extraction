import tweepy
import json
import argparse
import logging
import numpy as np
import pandas as pd
from prettytable import PrettyTable

# logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.INFO)
logging.basicConfig(format='[%(levelname)s][%(asctime)s]: %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.INFO)


def search_tweets_default(api, username, count):
    logging.info('Default')
    logging.info(f'Buscando curtidas de: {username}')
    logging.info('Extração de tweets iniciada')
    logging.info(f'Extraindo {count} tweets')
    tweets = api.favorites(screen_name=username,
                           count=count, tweet_mode="extended")
    logging.info('Extração de tweets finalizada')
    tweets_data = [tweet._json for tweet in tweets]
    return tweets_data


def search_tweets(api, username, count):
    rest = count % 200
    div = int((count - rest)/200)
    requests = [200 for i in list(range(0, div))]

    if (rest != 0):
        requests.append(rest)

    logging.info(f'Buscando curtidas de: {username}')
    logging.info('Extração de tweets iniciada')
    tweets = api.favorites(screen_name=username,
                           count=requests[0], tweet_mode="extended")
    logging.info(f'Extraindo {len(tweets)}/{count} tweets')
    tweets_data = [tweet._json for tweet in tweets]
    tweets_collection = tweets_data.copy()

    for n in requests[1:]:
        try:
            tweets = api.favorites(screen_name=username,
                                   count=n,
                                   tweet_mode="extended",
                                   max_id=tweets[len(tweets)-1]._json['id']-1)

            if(len(tweets) == 0):
                logging.info('A extração atingiu seu limite.')
                logging.info(
                    f'{len(tweets_collection)}/{count} tweets extraídos')
                break
            else:
                tweets_data = [tweet._json for tweet in tweets]
                tweets_collection = tweets_collection + tweets_data
                logging.info(
                    f'Extraindo {len(tweets_collection)}/{count} tweets')

        except tweepy.RateLimitError:
            logging.info('Rate Limit atingido')
            break

    logging.info('Extração de tweets finalizada')
    return tweets_collection


def to_JSON(tweets, filename):
    filename = filename.replace('@', '')
    logging.info(f'Criando o arquivo {filename}.json')
    with open(f'{filename}.json', 'w') as writer:
        json.dump(tweets, writer, indent=4, ensure_ascii=False)
    logging.info(f'{filename}.json criado.')


def from_JSON(filename):
    logging.info(f'Lendo o arquivo {filename}')
    with open(filename, 'r') as file:
        tweets = json.load(file)
    return tweets


def top_users_liked(tweets, num_users, rank_filename):
    logging.info(f'Computando os {num_users} usuários mais curtidos')
    screen_names = np.array([tweet['user']['screen_name'] for tweet in tweets])
    user, count = np.unique(screen_names, return_counts=True)
    df = pd.DataFrame({'user': user, 'count': count})
    df = df.sort_values(by=['count'], ascending=False)
    df = df.reset_index()

    table = PrettyTable()
    table.field_names = ["position", "user", "likes"]
    for i, j in enumerate(df.index):
        table.add_row([i+1, df['user'][j], df['count'][j]])
    
    with open(f'{rank_filename}.txt', 'w') as w:
        w.write(str(table))

    return table.get_string(start=0, end=num_users)


def main():
    
    parser = argparse.ArgumentParser(prog='get_liked_tweets.py')

    # argumentos
    parser.add_argument(
        '--username', type=str, help='Username do perfil, acompanhado do @')
    parser.add_argument(
        '--count', type=int, default=200, help='Quantidade de tweets para extração')
    parser.add_argument(
        '--input_file', help='Nome do arquivo de entrada')
    parser.add_argument(
        '--output_file', type=str, help="Nome do arquivo de saída")
    parser.add_argument(
        '--ranking', type=int, default=10, help='Número de posições do ranking')
    parser.add_argument(
        '--ranking_file', type=str, default='likes_ranking', help='Nome do arquivo do ranking completo')

    args = parser.parse_args()

    logging.info('Execução do Script iniciada.')

    if(args.input_file):
        tweets = from_JSON(args.input_file)
    else:
        # leitura dos tokens de acesso à API
        with open('tokens.json', 'r') as file:
            tokens = json.load(file)

        # gerando conexão com a API
        auth = tweepy.OAuthHandler(tokens['api_key'], tokens['api_secret_key'])
        auth.set_access_token(tokens['access_token'],
                              tokens['access_token_secret'])
        api = tweepy.API(auth)

        # count
        if(args.count <= 200):
            tweets = search_tweets_default(
                api=api, username=args.username, count=args.count)
        else:
            tweets = search_tweets(
                api=api, username=args.username, count=args.count)

        # output_file
        if(args.output_file):
            to_JSON(tweets=tweets, filename=args.output_file)
        else:
            to_JSON(tweets=tweets, filename=args.username)

    # ranking
    print(top_users_liked(tweets=tweets, num_users=args.ranking, rank_filename=args.ranking_file))

    logging.info('Execução do script finalizada.')


if __name__ == "__main__":
    main()
