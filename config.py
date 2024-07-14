import configparser

config = configparser.ConfigParser()
config.read("config.ini")

DATABASE_URL = config["database"]["DATABASE_URL"]
OPENAI_KEY = config["openai"]["OPENAI_KEY"]
