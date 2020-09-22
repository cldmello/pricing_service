import os
from typing import List
from requests import Response, post

class MailgunException(Exception):
  def __init__(self, message: str):
    self.message = message

class Mailgun:
  FROM_TITLE = "Pricing Service"
  FROM_ADDRESS = "do-not-reply@sandbox7cc8d82402604bca98fd3080cdbc0d8d.mailgun.org"
  @classmethod
  def send_mail(cls, address: List[str], subject: str, text: str, html: str) -> Response:
    api_key = os.environ.get('MAILGUN_API_KEY', None)
    domain = os.environ.get('MAILGUN_DOMAIN', None)

    if api_key is None:
      raise MailgunException('Error getting API Key for Mailgun.')
    if domain is None:
      raise MailgunException('Cannot locate Mailgun domain.')
    response = post(
                f"{domain}/messages",
                auth=("api", api_key),
                data={"from": f"{cls.FROM_TITLE} <{cls.FROM_ADDRESS}>",
                  "to": address,
                  "subject": subject,
                  "text": text,
                  "html": html})
    
    if response.status_code != 200:
      raise MailgunException('An error occurred while sending email via Mailgun.')

    return response
