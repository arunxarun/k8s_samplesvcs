import sys
sys.path.append('./src')  # tests are meant to be called from parent directory!
import pytest
from mock import patch, Mock
import json
import logging

from server import Svc1, Svc2
import requests

@patch.object(Svc2, 'get')
def testValidResponseFromSvc1(get_mock):
    get_mock.return_value = {'response': {'service':'SVC2', 'value': '256'}}
    svc2 = Svc2()
    svc1 = Svc1(Svc2)

    results = svc1.get("test value")

    assert(results.has_key('response'))
    assert(results['response'].has_key('value'))
    assert(results['response']['service'] == 'SVC2')
    assert(results['response']['value'] == '256')


@patch.object(requests,'get')
def testValidResponseFromSvc2(get_mock):

    ret_payload = Mock()
    ret_payload.json.return_value = {'response': {'service':'SVC2', 'value':'256'}}
    get_mock.return_value = ret_payload

    svc2 = Svc2()

    results = svc2.get('256')

    assert(results['response'] == {'service':'SVC2', 'value':'256'})
