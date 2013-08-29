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
    out: /usr/local/www/build

include:
    build.css:
        <<   : *options
        files:
            - ../../file1.css
            - ../../file2.css

    build.js:
        <<   : *options
        files:
            - ../../file1.js
            - ../../file2.js

        paths:
            - ../../path1
            - ../../path2
```

```
include.py --config='/usr/local/www/config/include.yaml'
```























##

* Include library is licensed under the MIT (MIT_LICENSE.txt) license

* Copyright (c) 2013 [Alexander Guinness] (https://github.com/monolithed)