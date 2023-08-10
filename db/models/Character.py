from mongoengine import StringField, IntField, Document, ListField, DictField


class Character(Document):
    id = IntField(primary_key=True)
    roleplay_id = IntField(required=True)
    name = StringField()

    inventory = DictField()
    fields = DictField()

    meta = {
        'collection': 'characters'
    }
