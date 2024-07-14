import configparser

config = configparser.ConfigParser()
config.read("config.ini")

DATABASE_URL = config["database"]["DATABASE_URL"]

OPENAI_KEY = config["openai"]["OPENAI_KEY"]

EMAIL_HOST = config["email"]["EMAIL_HOST"]
EMAIL_USER = config["email"]["EMAIL_USER"]
EMAIL_PASSWORD = config["email"]["EMAIL_PASSWORD"]
