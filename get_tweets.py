import tweepy
import json
import pymongo
import argparse
import logging


def search_tweets_default(api, q, lang, count=100):
    # logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.INFO)
    logging.basicConfig(format='[%(levelname)s][%(asctime)s]: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.INFO)
    logging.info('Extraindo tweets no modo DEFAULT')
    logging.info(f'Busca pelos termos: {q}')
    logging.info('Extração de tweets iniciada')
    logging.info(f'Extraindo {count} tweets')
    tweets = api.search(q=q, count=count, tweet_mode="extended", lang=lang)
    logging.info('Extração de tweets finalizada')
    tweets_data = [tweet._json for tweet in tweets]
    return tweets_data


def search_tweets(api, q, lang, count=100):
    # logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.INFO)
    logging.basicConfig(format='[%(levelname)s][%(asctime)s]: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.INFO)
    logging.info('Extraindo tweets no modo EXTENDED')
    logging.info(f'Busca pelos termos: {q}')
    logging.info('Extração de tweets iniciada')
    tweets = api.search(q=q, count=count, tweet_mode="extended", lang=lang)
    tweets_data = [tweet._json for tweet in tweets]
    logging.info(f'Extraindo {len(tweets_data)} tweets')
    tweets_collection = tweets_data.copy()

    while(len(tweets) != 0):
        try:
            tweets = api.search(q=q,
                                count=count,
                                tweet_mode="extended",
                                lang=lang,
                                max_id=tweets[len(tweets)-1]._json['id']-1)

            tweets_data = [tweet._json for tweet in tweets]
            # collection.insert_many(tweets_data)

            tweets_collection = tweets_collection + tweets_data
            logging.info(f'Extraindo {len(tweets_collection)} tweets')

        except tweepy.RateLimitError:
            logging.info('Rate Limit atingido')
            logging.info('Extração de tweets finalizada')
            break

    return tweets_collection


def to_txt(tweets, filename):
    logging.basicConfig(format='[%(levelname)s][%(asctime)s]: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.INFO)
    logging.info(f'Criando o arquivo {filename}.txt')
    with open(f'{filename}.txt', 'a') as writer:
        json.dump(tweets, writer, indent=4, ensure_ascii=False)
    logging.info(f'{filename}.txt criado.')


def main():
    parser = argparse.ArgumentParser(prog='get_tweets.py')

    # parser.add_argument('tokens')
    parser.add_argument(
        'query', type=str, help='Palavra ou lista de palavras (separadas por vírgulas).')
    parser.add_argument(
        'out', type=str, help='Nome do arquivo .txt contendo os tweets.')
    parser.add_argument(
        '--lang', type=str, help='Idioma dos tweets.', default='')
    parser.add_argument(
        '--mode', help='Modo de extração dos tweets.', choices=['default', 'extended'], default='default')

    args = parser.parse_args()

    with open('tokens.json', 'r') as file:
        tokens = json.load(file)

    auth = tweepy.OAuthHandler(tokens['api_key'], tokens['api_secret_key'])
    auth.set_access_token(tokens['access_token'],
                          tokens['access_token_secret'])
    api = tweepy.API(auth)

    if(args.mode == 'extended'):
        tweets = search_tweets(
            api=api, q=args.query.split(','), lang=args.lang)
    else:
        tweets = search_tweets_default(
            api=api, q=args.query.split(','), lang=args.lang)

    to_txt(tweets=tweets, filename=args.out)


if __name__ == "__main__":
    main()
