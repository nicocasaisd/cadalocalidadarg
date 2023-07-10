import tweepy
import logging
import os

logger = logging.getLogger()

def create_api():
    #   Usa os para leer las environment variables
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")


    # Crea el objeto auth
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Crea el objeto API
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # Verifica que las credenciales sean válidas
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API Created")
    return api


def create_api_v2():
    #   Usa os para leer las environment variables
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    bearer_token = os.getenv("BEARER_TOKEN")


    # Crea el objeto Client
    client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret, wait_on_rate_limit=True)
    # Verifica que las credenciales sean válidas
    # try:
    #     api.verify_credentials()
    # except Exception as e:
    #     logger.error("Error creating API", exc_info=True)
    #     raise e
    # logger.info("API Created")
    return client
