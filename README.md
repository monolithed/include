# Include

Include - A simple file builder


## Synopsis

```
include.py --config [ --test ] | [ --version ]
```


## Dependencies

```
pip install pyyaml
```


## Usage


*/usr/local/www/config/include.yaml*

```yaml
default: &options
    route: /usr/local/www/build

include:
    build.css:
        <<   : *options
        files:
            - /usr/local/www/build/file1.css
            - /usr/local/www/build/file2.css

    build.js:
        <<   : *options
        files:
            - /usr/local/www/build/file1.js
            - /usr/local/www/build/file2.js
```

```
include.py --config='/usr/local/www/config/include.yaml'
```























##

* Include library is licensed under the MIT (MIT_LICENSE.txt) license

* Copyright (c) 2013 [Alexander Guinness] (https://github.com/monolithed)