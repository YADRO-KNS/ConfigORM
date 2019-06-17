# ConfigORM
[![Build Status](https://travis-ci.com/YADRO-KNS/ConfigORM.svg?branch=master)](https://github.com/YADRO-KNS/ConfigORM)

----

Heavily inspired by Charles Leifer [peewee](https://github.com/coleifer/peewee) ORM.
This package provides ORM-like interface to interact with *.ini configs. 
And map their data onto object models.



Examples
--------
Lets say we have config like this:
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

Defining models is similar to ORM's:
```python
#Config.py

import os
from configorm import *

current_dir = os.path.abspath(os.path.dirname(__file__))
connection_string = os.path.join(current_dir, 'config.ini')

connector = IniConnector(connection_string=connection_string)

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

Section names must match their counterparts in ini file, but case does not matter at all.
All spaces in section or key names of config file will be treated as underlines. 


Depending on field data will be casted to exact type.
```
>>> from Config import General
>>> General.debug
True
>>> type(General.debug)
<class 'bool'>
```


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


Base Section aside from connection to config file also provides tool to create
 configuration from models, allowing model-first approach. It crates config file,
 sections from your models names and option based on provided fields. In case if
 fields have default values, they will be written in config as well. Otherwise
 options will be filled with empty values.
 
```
>>> from Config import *
>>> BaseSection.check_config_integrity()
```
