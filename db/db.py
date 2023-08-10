from mongoengine import connect
from config import mongo_url

from .models.Character import Character
from .models.Roleplay import Roleplay


class Database:
    def __init__(self):
        self.connection = connect(host=mongo_url, db='roleplay_systems')

    def get_roleplays(self, chat_id):
        return Roleplay.objects(chat_id=chat_id)
