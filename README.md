APIBridge
=========

Joining **json** API calls together

---

[![Build Status](https://travis-ci.org/robin-weiland/APIBridge.svg?branch=master)](https://travis-ci.org/robin-weiland/APIBridge)
[![codecov](https://codecov.io/gh/robin-weiland/APIBridge/branch/master/graph/badge.svg)](https://codecov.io/gh/robin-weiland/APIBridge)
[![PyPI version](https://badge.fury.io/py/apibridge.svg)](https://badge.fury.io/py/apibridge)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)

---

# Installation

```batch
pip install api_bridge
```

# Usage

## The API-class

````python
API(url: str,
    method: Method = Method.GET,
    result_filter: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    validate: Optional[Callable[[Dict[str, Any]], bool]] = None,
    post_data: Optional[Dict[str, Any]] = None
    )
````

*url* The url to run a request with

*method* The Enum from `api_bridge.methods.Method` [either `Method.GET` or `.POST`; defaults to `.GET`]

*result_filter* A filter for the retrieved json data `api_bridge.filter.Filter` [defaults to `None`]

 ---
 
````python
Filter(**out: str)
````
*out* The items of the filtered data

examples:

````python
Filter(lat='latitude', long='longitude')  # {'lat': data['latitude'], 'long': data['longitude']}

Filter(sunrise='results sunrise')  # spaces represent {'sunrise': data['results]['sunrise']}
````

---

*validate* An additional test based on the received data in addition to the http-status-code [defaults to None]

example:

````python
validate=lambda data: data['status'] == 'successful'
````

*post_data* Data if `Method.POST` was provided



    


## Requests

There are two ways to run a request

````python
from api_bridge.api import API
from api_bridge.filter import Filter
from api_bridge.container import Container

LOCATION_URL = 'https://ipapi.co/json/'
TIME_URL = 'https://api.sunrise-sunset.org/json?lat={lat}&lng={long}&date=today'
````

The `chain`-method
```python
result = API.chain(
            API(LOCATION_URL, result_filter=Filter(lat='latitude', long='longitude')),
            API(TIME_URL, validate=lambda response: response['status'] == 'OK', result_filter=Filter(sunrise='results sunrise'))
         )

result == {'sunrise': '4:08:10 AM'}
```

The (esoteric) operator-method ```>``` or ```>>```
````
result = API('https://ipapi.co/json/', result_filter=Filter(lat='latitude', long='longitude')) > \
                API('https://api.sunrise-sunset.org/json?lat={lat}&lng={long}&date=today', validate=lambda response:
                    response['status'] == 'OK', result_filter=Filter(sunrise='results sunrise')) > \
                Container()

result == {'sunrise': '4:08:10 AM'}
````

> *Important* the gt and rshift operator mehtod must terminate with an ````Operator()````, which can be treated a dict afterwards
