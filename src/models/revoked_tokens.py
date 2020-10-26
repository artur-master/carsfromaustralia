from src.services.db import db


class RevokedToken(db.Document):
    jti = db.StringField(required=True, unique=True)
