from amazonregister import AmazonService
from googleregister import GoogleService
from microsoftregister import MicrosoftService
# need to pip install -U pytest
# to run: python -m pytest dbtest.py


def test_get_instance_info():
  service = AmazonService()
  assert isinstance(service.get_instances_info(), list)

  service = GoogleService()
  assert isinstance(service.get_instances_info(), list)

  service = MicrosoftService()
  assert isinstance(service.get_instances_info(), list)
