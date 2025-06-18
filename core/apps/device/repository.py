import abc
import logging
from django.apps import apps
from django.db import transaction
from django.db.models import QuerySet
from django.db.models import Model


logger = logging.getLogger(__name__)


class AbstractRepository(abc.ABC):

    def get(self, **kwargs) -> None:
        raise NotImplementedError

    def get_all(self) -> None:
        raise NotImplementedError

    def create(self, **kwargs) -> None:
        raise NotImplementedError

    def update(self, **kwargs) -> None:
        raise NotImplementedError

    def delete(self, **kwargs) -> None:
        raise NotImplementedError


class Repository(AbstractRepository):
    def __init__(self, model: str):
        self.model = apps.get_model("device", model)

    def get(self, **kwargs) -> Model:
        return self.model.objects.get(**kwargs)

    def get_all(self) -> QuerySet:
        return self.model.objects.all()

    def create(self, **kwargs) -> Model:
        return self.model.objects.create(**kwargs)

    def get_or_create(self, defaults=None, **kwargs) -> tuple[Model, bool]:
        return self.model.objects.get_or_create(defaults=None, **kwargs)

    @staticmethod
    def update(obj, **kwargs) -> Model:
        obj.update(**kwargs)
        obj.save()
        return obj

    def delete(self, **kwargs) -> None:
        obj = self.get(**kwargs)
        obj.delete()
