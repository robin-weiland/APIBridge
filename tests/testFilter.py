#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-15"
__version__ = "0.0.2"

__all__ = ()

from api_bridge.filter import Filter
from unittest import TestCase


class FilterTest(TestCase):
    def testFilterNonFlat(self):
        data = {
            'results': {'sunrise': '4:06:40 AM', 'sunset': '6:33:30 PM', 'solar_noon': '11:20:05 AM',
                        'day_length': '14:26:50', 'civil_twilight_begin': '3:30:47 AM',
                        'civil_twilight_end': '7:09:23 PM', 'nautical_twilight_begin': '2:45:20 AM',
                        'nautical_twilight_end': '7:54:50 PM', 'astronomical_twilight_begin': '1:52:18 AM',
                        'astronomical_twilight_end': '8:47:52 PM'},
            'status': 'OK'
        }

        self.expected = {'sunrise': '4:06:40 AM'}
        f = Filter(snrise='results sunrise')

    def testFilterFlat(self):
        data = {
            'ip': '127.0.0.1',
            'city': 'Town',
            'region': 'Region',
            'region_code': 'hahaha',
            'country': 'DE',
            'country_code': 'DE',
            'country_code_iso3': 'DEU',
            'country_capital': 'Berlin',
            'country_tld': '.de',
            'country_name': 'Germany',
            'continent_code': 'EU',
            'in_eu': True,
            'postal': '00000',
            'latitude': 48.3214,
            'longitude': 9.7864,
            'timezone': 'Europe/Berlin',
            'utc_offset': '+0200',
            'country_calling_code': '+49',
            'currency': 'EUR',
            'currency_name': 'Euro',
            'languages': 'de',
            'country_area': 357021.0,
            'country_population': 81802257.0,
            'asn': 'whatever',
            'org': 'some isp'
        }
        expected = dict(lat=48.3214, long=9.7864)
        f = Filter(lat='latitude', long='longitude')

        self.assertDictEqual(
            expected,
            f(data),
            'Filter did not perform correctly!'
        )


if __name__ == '__main__': pass
