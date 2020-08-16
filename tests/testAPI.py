#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-15"
__version__ = "0.0.2"

__all__ = ()

from api_bridge.api import API
from api_bridge.filter import Filter
from api_bridge.container import Container
from api_bridge.methods import Method
from api_bridge.exceptions import APIException, ValidationException

from unittest import TestCase

from requests import get

LOCATION_URL = 'https://ipapi.co/json/'
TIME_URL = 'https://api.sunrise-sunset.org/json?lat={lat}&lng={long}&date=today'
FAIL_URL = 'https://httpbin.org/status/500'
POST_URL = 'https://httpbin.org/post'


def referenceAPI():
    location = get(LOCATION_URL).json()
    time = get(TIME_URL.format(lat=location['latitude'], long=location['longitude'])).json()
    return {'sunrise': time['results']['sunrise']}


class APITest(TestCase):
    def testChain(self):
        result = (API.chain(
            API(LOCATION_URL, result_filter=Filter(lat='latitude', long='longitude')),
            API(TIME_URL,
                validate=lambda response: response['status'] == 'OK', result_filter=Filter(sunrise='results sunrise'))
        ))

        container = Container()
        container.value = referenceAPI()
        self.assertEqual(
            container.value,
            result.value,
            'The chain operator does not work properly!'
        )

    def testCall(self):
        result = API('https://ipapi.co/json/', result_filter=Filter(lat='latitude', long='longitude')) > \
                 API('https://api.sunrise-sunset.org/json?lat={lat}&lng={long}&date=today', validate=lambda response:
                     response['status'] == 'OK', result_filter=Filter(sunrise='results sunrise')) > \
                 Container()
        container = Container()
        container.value = referenceAPI()
        # noinspection PyUnresolvedReferences
        self.assertEqual(
            container.value,
            result.value,
            'The call operator does not work properly!'
        )

    def testInvalidURL(self):
        self.assertRaises(
            APIException,
            API.chain,
            API('test:hello:world')
        )

    def testJsonNoRequest(self):
        self.assertRaises(
            APIException,
            API(LOCATION_URL).json
         )

    def testBadResponse(self):
        self.assertRaises(
            ValidationException,
            API.chain,
            API(FAIL_URL)
        )

    def testFailedValidation(self):
        self.assertRaises(
            APIException,
            API.chain,
            API(POST_URL,
                method=Method.POST,
                post_data={'success': 'False'},
                validate=lambda data: data['form']['success'] == 'True')
        )

    def testInit(self):
        validate = lambda data: 'latitude' in data and 'longitude' in data
        api = API(url=LOCATION_URL,
                  method=Method.POST,
                  result_filter=Filter(lat='latitude', long='longitude'),
                  validate=validate,
                  post_data=dict(date='today'))

        self.assertEqual(LOCATION_URL,
                         api.url,
                         'Url not passed properly!')

        self.assertEqual(Method.POST,
                         api.method,
                         'Method not passed properly!')

        self.assertEqual(Filter(lat='latitude', long='longitude'),
                         api.result_filter,
                         'Filter not passed properly!')

        self.assertEqual(validate,
                         api.validate,
                         'Validate not passed properly!')

        self.assertEqual(dict(date='today'),
                         api.post_data,
                         'Post-Data not passed properly!')


if __name__ == '__main__': pass
