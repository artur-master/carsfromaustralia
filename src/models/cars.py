import json
from src.services.db import db


class Car(db.Document):
    """ Common fields """
    url = db.StringField(required=True, unique=True)
    updated = db.StringField(required=True)
    name = db.StringField(required=True)
    price = db.DictField(required=True)
    year = db.IntField(required=True)
    odometer = db.IntField(required=True)
    make = db.StringField(required=True)
    body_type = db.StringField(required=True)
    model = db.StringField(required=True)
    color = db.StringField(required=True)
    engine_size = db.FloatField(required=True)
    seat = db.StringField(required=True)
    drive = db.StringField(required=True)
    compliance = db.StringField(required=True)
    transmission = db.StringField(required=True)
    cylinders = db.IntField(required=True)
    images = db.ListField(required=True)
    vin = db.StringField(required=True)
    fuel = db.StringField(required=True)
    variant = db.StringField(required=True)
    description = db.StringField(required=True)
    engine_size_unit = db.StringField(required=True)
    location = db.StringField(required=True)

    """ Additional(Virtual yard)"""
    builtDate = db.StringField(required=True)
    advKms = db.IntField(required=True)
    contact = db.StringField(required=True)
    engneNo = db.StringField(required=True)
    redbookCode = db.StringField(required=True)
    rego = db.StringField(required=True)
    regoExpiry = db.StringField(required=True)

    """ Additional(pickles) """
    door = db.IntField(required=True)
    wovr = db.StringField(required=True)
    manufacturer_color = db.StringField(required=True)
    series = db.StringField(required=True)
    trim_color = db.StringField(required=True)
    trim_type = db.StringField(required=True)
    gear = db.StringField(required=True)
    induction = db.StringField(required=True)
    build_year = db.IntField(required=True)
    features = db.StringField(required=True)
    ancap = db.StringField(required=True)

    def serialize(self, excludes=None):
        car = {
            'id': str(self.id),
            'url': self.url,
            'updated': self.updated,
            'name': self.name,
            'price': self.price,
            'year': self.year,
            'odometer': int(self.odometer/1.609344),
            'make': self.make,
            'body_type': self.body_type,
            'model': self.model,
            'color': self.color,
            'engine_size': self.engine_size,
            'seat': self.seat,
            'drive': self.drive,
            'compliance': self.compliance,
            'transmission': self.transmission,
            'cylinders': self.cylinders,
            'images': self.images,
            'vin': self.vin,
            'fuel': self.fuel,
            'variant': self.variant,
            'description': self.description,
            'engine_size_unit': self.engine_size_unit,
            'location': self.location,

            'builtDate': self.builtDate,
            'advKms': self.advKms,
            'contact': self.contact,
            'engneNo': self.engneNo,
            'redbookCode': self.redbookCode,
            'rego': self.rego,
            'regoExpiry': self.regoExpiry,

            'door': self.door,
            'wovr': self.wovr,
            'manufacturer_color': self.manufacturer_color,
            'series': self.series,
            'trim_color': self.trim_color,
            'trim_type': self.trim_type,
            'gear': self.gear,
            'induction': self.induction,
            'build_year': self.build_year,
            'features': self.features,
            'ancap': self.ancap,
        }

        if excludes is not None:
            for field in excludes:
                del car[field]

        return car
