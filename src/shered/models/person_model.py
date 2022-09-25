from peewee import *
from .base_model import BaseModel


class PersonModel(BaseModel):
    person_id = IdentityField()
    person_name = CharField(max_length=255)
    person_age = IntegerField()
    person_address = CharField(max_length=255)
    person_work = CharField(max_length=255)

    def as_dict(self) -> dict:
        return {
            'id': self.person_id,
            'name': self.person_name,
            'age': self.person_age,
            'address': self.person_address,
            'work': self.person_work,
        }

    @staticmethod
    def get_signature():
        return {
            'name': str,
            'age': int,
            'address': str,
            'work': str
        }

    class Meta:
        db_table = "person"
