from typing import Union

from discord import User, Member
from peewee import Model, SqliteDatabase, BigIntegerField, IntegerField, CharField

general_database = SqliteDatabase('general.db')


class GeneralBaseModel(Model):
    class Meta:
        database = general_database


class ProfileModel(GeneralBaseModel):
    uid = BigIntegerField(primary_key=True)
    age = IntegerField(default=0)
    bio = CharField(max_length=2012, default="None")
    gender = CharField(max_length=255, default="Undefined")

    @classmethod
    def get_or_insert(cls, user: Union[User, Member, int]) -> 'ProfileModel':
        if hasattr(user, 'id'):
            user = user.id
        model, created = cls.get_or_create(uid=user)
        if created:
            model.save()
        return model

    @property
    def display_age(self):
        if self.age < 13:
            return '< 13'
        last_age = 12
        for next_age in [18, 29, 39, 49, 59, 69, 89, 109, 129]:
            if self.age <= next_age:
                return f'{last_age+1}-{next_age}'
            last_age = next_age
        return '130+'


ProfileModel.create_table(safe=True)
