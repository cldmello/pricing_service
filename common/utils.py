import re
from passlib.hash import pbkdf2_sha512

class Utils:
  @staticmethod
  def email_is_valid(email: str) -> bool:
    email_pattern = re.compile(r'^[\w-]+@([\w-]+\.)+[\w]+$')
    return True if email_pattern.match(email) else False

  @staticmethod
  def hash_password(password: str) -> str:
    return pbkdf2_sha512.encrypt(password)

  @staticmethod
  def check_hash_password(password: str, hash: str) -> bool:
    return pbkdf2_sha512.verify(password, hash)
