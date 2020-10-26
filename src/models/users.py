import json
from src.services.db import db


class User(db.Document):
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, unique=False)
    first_name = db.StringField(required=True, unique=False)
    last_name = db.StringField(required=True, unique=False)
    role = db.StringField(required=True, unique=False)

    verified = db.BooleanField()
    verified_at = db.DateTimeField()

    active = db.BooleanField()
    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()

    def serialize(self, excludes=None):
        user = {
            'id': str(self.id),
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,

            'verified': self.verified,
            'active': self.active
        }
        if self.verified_at is not None:
            user['verified_at'] = self.verified_at.strftime("%Y-%m-%d %H:%M:%S")

        if self.created_at is not None:
            user['created_at'] = self.created_at.strftime("%Y-%m-%d %H:%M:%S")

        if self.updated_at is not None:
            user['updated_at'] = self.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        if excludes is not None:
            for field in excludes:
                del user[field]

        return user
