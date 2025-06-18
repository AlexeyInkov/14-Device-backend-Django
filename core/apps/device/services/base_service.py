from django.db.models import Model, QuerySet


class BaseService:
    repository = None

    @classmethod
    def get(cls, **kwargs) -> Model:
        return cls.repository.get(**kwargs)

    @classmethod
    def get_all(cls) -> QuerySet:
        return cls.repository.get_all()

    @classmethod
    def create(cls, **kwargs) -> Model:
        return cls.repository.create(**kwargs)

    @classmethod
    def get_or_create(cls, defaults=None, **kwargs):
        return cls.repository.get_or_create(defaults, **kwargs)

    @classmethod
    def update(cls, **kwargs) -> Model:
        return cls.repository.update(**kwargs)

    @classmethod
    def delete(cls, **kwargs) -> None:
        return cls.repository.delete(**kwargs)
