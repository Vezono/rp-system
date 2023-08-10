from mongoengine import StringField, IntField, Document, ListField, DictField


class Roleplay(Document):
    id = IntField(primary_key=True)
    chat_id = IntField(required=True)
    title = StringField()

    users = ListField()  # поки що не використовується
    characters = ListField()

    default_fields = DictField()


    meta = {
        'collection': 'roleplays'
    }
