# cumbiabot/config.py
import tweepy
import logging
import os

logger = logging.getLogger()

def create_api():
#    Usa os para leer las environment variables
    # consumer_key = os.environ["CONSUMER_KEY"]
    # consumer_secret = os.environ["CONSUMER_SECRET"]
    # access_token = os.environ["ACCESS_TOKEN"]
    # access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

    #   Usa os para leer las environment variables
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    # consumer_key="XWJjkGgLsAfeRFafCeT5FrLNQ"
    # consumer_secret="qgynIk13XyPjdynbrweBkqFmsiRuRcsFqFK5yys1ABGKAthHn1"
    # access_token="1550598025466331136-XpXH6pOswtIJexAWPyXc6ljyXyWPUp"
    # access_token_secret="DU4LOnDYIlgByYRdyWIBj6Rgbzevw71tP6FvxcmvcL3vV"

    # Crea el objeto auth
#    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#    auth.set_access_token(access_token, access_token_secret)
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
