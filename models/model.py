from typing import Dict, List, TypeVar, Type, Union
from abc import ABCMeta, abstractmethod
from common.database import Database

T = TypeVar('T', bound='Model')

class Model(metaclass=ABCMeta):
  collection: str
  _id: str

  def __init__(self, *args, **kwargs):
    pass
  # The above lines are code are to avoid abstract class errors in IDE

  @abstractmethod
  def json(self) -> Dict:
    raise NotImplementedError

  def save_to_mongo(self):
    Database.update(self.collection, {"_id": self._id}, self.json())

  def remove_from_mongo(self):
      Database.remove(self.collection, {"_id": self._id})

  @classmethod
  def all(cls: Type[T]) -> List[T]:
    db_list = Database.find(cls.collection, {})
    return [cls(**list_item) for list_item in db_list]

  @classmethod
  def find_one_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> T:
    return cls(**Database.find_one(cls.collection, {attribute: value}))

  @classmethod
  def find_many_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> List[T]:
    return [cls(**elem) for elem in Database.find(cls.collection, {attribute: value})]

  @classmethod
  def get_by_id(cls: Type[T], _id: str) -> T: # Item.get_by_id -> Item & Alert.get_by_id -> Alert
    return cls.find_one_by("_id", _id)