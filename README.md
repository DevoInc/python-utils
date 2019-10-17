[![relese-next Build Status](https://travis-ci.com/DevoInc/python-utils.svg?branch=master)](https://travis-ci.com/DevoInc/python-utils) [![LICENSE](https://img.shields.io/dub/l/vibe-d.svg)](https://github.com/DevoInc/python-utils/blob/master/LICENSE)

[![wheel](https://img.shields.io/badge/wheel-yes-brightgreen.svg)](https://pypi.org/project/devo-utils/) [![version](https://img.shields.io/badge/version-2.0.1-blue.svg)](https://pypi.org/project/devo-utils/) [![python](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue.svg)](https://pypi.org/project/devo-utils/)


# Devo Python Utils

This package it's an extra for the Devo SDK and our clients. It can be used to:
* Order files.
* Generate fake data.
* File IO generators.

## Requirements

This package require Python 3.5+ and devo-sdk package

## Quick Start
### Installing the package:

You can install the Devo SDK by using `easy_install` or `pip`:

    #option 1
    easy_install devo-utils
    
    #option 2
    pip install devo-utils


You can use sources files, clonning the project too:

    #option 3
    python setup.py install
    
    #option 4
    pip install .
    
    #option 5 - dev option
    pip install -e .

### Documentation

You have specific documentation in _[docs](docs)_ folder for each part of SDK:
* [Faker: fake data](docs/faker.md)
* [File IO](docs/io/fileio.md)
* [Sorting data](docs/sorter.md)


## Contributing
See [Python Utils contributing guide](CONTRIBUTING.md).<br/>
Pull requests are welcome ☺

## Launch tests
### run_tests script
You can run tests from the main folder of SDK
To launch this script, you need either the environment variables loaded in the system, or the _environment.env_ file in the root of the SDK with the correct values, since to test all the SDK functionalities it is necessary to connect to Devo for the tests of sending and extracting data. You has a example file called _environment.env.example_

It's normal, by the way, TCP tests fails in clients or not Devo developers systems.

```bash
~/projects/python-utils > python setup.py test 
```

```bash
~/projects/python-utils > python run_tests.py
```

You can add option "Coverage" for create HTML report about tests.

```bash
~/projects/python-utils > python run_tests.py --coverage
```


### Run using Unittest command

You can see references in [unittest documentation](https://docs.python.org/3/library/unittest.html)

For commands like:

```bash
python -m unittest discover -p "*.py" 
```

If you launch this command from the root directory of the SDK, you need to have the environment variables in your 
system for all the tests that require connection to Devo can work, not being able to use the environment.env file 
as in the script.


### Contact Us

You can contact with us at _support@devo.com_.

## License
MIT License

(C) 2019 Devo, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the 'Software'), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
