import tweepy
import json
import argparse
import logging

# logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.INFO)
logging.basicConfig(format='[%(levelname)s][%(asctime)s]: %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.INFO)


def search_tweets_default(api, username, rts, replies, count=200):
    logging.info('Extraindo tweets no modo DEFAULT')
    logging.info(f'Busca por tweets do usuário {username}')
    logging.info('Extração de tweets iniciada')
    tweets = api.user_timeline(
        screen_name=username, tweet_mode="extended", include_rts=not(rts), exclude_replies=replies, count=count)
    logging.info(f'{len(tweets)} tweets extraídos')
    tweets_data = [tweet._json for tweet in tweets]
    logging.info('Extração de tweets finalizada')
    logging.info(f'Total de tweets extraídos: {len(tweets_data)}')
    return tweets_data


def search_tweets(api, username, rts, replies, count=200):
    logging.info('Extraindo tweets no modo EXTENDED')
    logging.info(f'Busca por tweets do usuário {username}')
    logging.info('Extração de tweets iniciada')
    tweets = api.user_timeline(
        screen_name=username, tweet_mode="extended", include_rts=not(rts), exclude_replies=replies, count=count)
    tweets_data = [tweet._json for tweet in tweets]
    logging.info(f'{len(tweets)} tweets extraidos')
    tweets_collection = tweets_data.copy()

    while(len(tweets) != 0):
        try:
            tweets = api.user_timeline(screen_name=username,
                                       tweet_mode="extended",
                                       include_rts=not(rts),
                                       exclude_replies=replies,
                                       count=count,
                                       max_id=tweets[len(tweets)-1]._json['id']-1)
            if (len(tweets) == 0):
                break
            else:
                tweets_data = [tweet._json for tweet in tweets]
                tweets_collection = tweets_collection + tweets_data
                logging.info(f'{len(tweets)} tweets extraidos')

        except tweepy.RateLimitError:
            logging.info('Rate Limit atingido')
            logging.info('Extração de tweets finalizada')
            break
    
    logging.info(f'Total de tweets extraídos: {len(tweets_collection)}')
    return tweets_collection


def to_txt(tweets, filename):
    filename = filename.replace('@', '')
    logging.info(f'Criando o arquivo {filename}.txt')
    with open(f'{filename}.txt', 'w') as writer:
        json.dump(tweets, writer, indent=4, ensure_ascii=False)
    logging.info(f'{filename}.txt criado.')


def main():
    parser = argparse.ArgumentParser(prog='get_tweets.py')

    parser.add_argument(
        '--username', type=str, help='Username do perfil, acompanhado do @', required=True)
    parser.add_argument(
        '--exclude_rts', help='Opção para incluir os retwwets da extração', action='store_true')
    parser.add_argument(
        '--exclude_replies', help='Opção para excluir os replies da extração', action='store_true')
    parser.add_argument(
        '--output', type=str, help='Nome do arquivo contendo os tweets')
    parser.add_argument(
        '--mode', help='Modo de extração dos tweets', choices=['default', 'extended'], default='default')

    args = parser.parse_args()

    with open('tokens.json', 'r') as file:
        tokens = json.load(file)

    auth = tweepy.OAuthHandler(tokens['api_key'], tokens['api_secret_key'])
    auth.set_access_token(tokens['access_token'],
                          tokens['access_token_secret'])
    api = tweepy.API(auth)
    
    if(args.mode == 'extended'):
        tweets = search_tweets(
            api=api, username=args.username, rts=args.exclude_rts, replies=args.exclude_replies)
    else:
        tweets = search_tweets_default(
            api=api, username=args.username, rts=args.exclude_rts, replies=args.exclude_replies)

    if(args.output):
        to_txt(tweets=tweets, filename=args.output)
    else:
        to_txt(tweets=tweets, filename=args.username)
    
    # print(args)

if __name__ == "__main__":
    main()
