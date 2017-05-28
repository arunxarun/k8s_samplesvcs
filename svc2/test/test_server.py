import sys
sys.path.append('./src')  # tests are meant to be called from parent directory!
import pytest
from mock import patch, Mock
import json
import logging

from server import  Svc2
import requests


def testValidResponseFromSvc2():

    svc2 = Svc2()

    results = svc2.get('256')

    assert(results['response'] == {'service':'Svc2', 'value':'256'})
