# ConfigORM
[![Build Status](https://travis-ci.com/YADRO-KNS/ConfigORM.svg?branch=master)](https://github.com/YADRO-KNS/ConfigORM)
![PyPI - Status](https://img.shields.io/pypi/status/ConfigORM.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ConfigORM.svg)
![PyPI](https://img.shields.io/pypi/v/ConfigORM.svg)
![PyPI - License](https://img.shields.io/pypi/l/ConfigORM.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ConfigORM.svg)
----

Heavily inspired by Charles Leifer [peewee](https://github.com/coleifer/peewee) ORM.
This package provides ORM-like interface to interact with *.ini configs and secrets in HashiCorp Vault. 
And map their data onto object models.

## Getting Started

### Installation
You can install ConfigORM with pip:
```
$ pip3 install ConfigORM
```

### Two Sources
The library supports two sources of data storage - ini-file and Vault by HashiCorp. The operation interface in this case will be identical.

### Quick Start ini-file way

Let's say we have config like this:
```ini
#config.ini

[Database]
server = 10.10.10.10
password = my_password
user = admin
base = test_base

[General]
debug = True
connection port = 5000
```

Create connection to the source:
```python
#Config.py

import os
from configorm import *

current_dir = os.path.abspath(os.path.dirname(__file__))
connection_string = os.path.join(current_dir, 'config.ini')

connector = IniConnector(connection_string=connection_string)
```

### Quick Start HashiCorp Vault way

Provide connection data for Vault server and KV store in it:
```python
#Config.py

from configorm import VaultConnector

connector = VaultConnector(
    mount_point='SOME_KV_STORE/',
    url='http://some-vault-url.com',
    token='TOKEN_FOR_SECRETS'
) 
```

### Defining models

Defining models is similar to ORM's:
```Python
#Config.py


class BaseSection(Section):
    class Meta:
        connector = connector
        
class Database(BaseSection):
    server = StringField()
    password = StringField()
    user = StringField()
    base = StringField()
    
class General(BaseSection):
    debug = BooleanField()
    connection_port = IntegerField()
    
```
```
>>> from Config import Database
>>> Database.server
'10.10.10.10'
```

Section names must match their counterparts in ini file or Vault, but case does not matter at all.
All spaces in section or key names of config file will be treated as underlines. 

#### Field Types

Depending on field data will be cast to exact type.
```
>>> from Config import General
>>> General.debug
True
>>> type(General.debug)
<class 'bool'>
```

Available Field Types:
* **StringField** 
* **IntegerField** 
* **BooleanField** 
* **FloatField** 
* **ListField** 

Most field types are self-explanatory, ListField is a bit tricky. It allows to store and 
extract data as list of homogeneous objects, such as strings, integers, floats and booleans.
You must provide exec type of stored objects.

```python
from configorm import *

class TestSection(Section):
    list_of_int = ListField(var_type=int)
    list_of_str = ListField(var_type=str)
    list_of_float = ListField(var_type=float)
    list_of_bool = ListField(var_type=bool)

```
 
#### Fallback Values

You may provide default fallback values for your fields.
If field may return None Type values, null parameter must be set as True

```python
from configorm import *

class Database(Section):
    server = StringField(default='10.10.10.10')
    password = StringField(default='secret')
    user = StringField(default='admin')
    base = StringField(default='development')
    
    possible_none_value = StringField(null=True)

```
 
#### Environment Variables Override
--------

You can override filed values with data from environment variables. Set 
**env_override** flag as True and if value is present in environment field
will attempt to use that. Environment key is formed from concatenation of 
section and field name in upper case. If value is missing from environment 
variables field will use standard approach. 

```python
from configorm import *
import os

class SomeSection(Section):
    le_field = StringField(default='value', env_override=True)
    
os.environ['SOMESECTION_LE_FIELD'] = 'env_value'

```

#### Model First Approach

Base Section aside from connection to config file also provides tool to create
 configuration from models, allowing model-first approach. It crates config file,
 sections from your models names and option based on provided fields. In case if
 fields have default values, they will be written in config as well. Otherwise,
 options will be filled with empty values. Works with both ini and Vault connections.
 
```
>>> from Config import *
>>> BaseSection.check_config_integrity()
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Hat tip to Charles Leifer for Inspiration
