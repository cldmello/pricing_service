import uuid
from typing import Dict
import requests
import re
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from models.model import Model

@dataclass(eq=False)
class Item(Model):
  collection: str = field(init=False, default="items")
  url: str
  tag: str
  query: Dict
  price: float = field(default=None)
  _id: str = field(default_factory=lambda: uuid.uuid4().hex)

  def load_price(self):
    response = requests.get(self.url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    element = soup.find(self.tag, self.query)
    string_price = element.text.strip()

    pattern = re.compile(r"(\d+,?\d+\.\d\d)")
    match = pattern.search(string_price)
    price_found = match.group(1)
    sans_comma = price_found.replace(",", "")
    self.price = float(sans_comma)
    return self.price

  def json(self) -> Dict:
    return {
      "_id": self._id,
      "url": self.url,
      "tag": self.tag,
      "price": self.price,
      "query": self.query
    }
