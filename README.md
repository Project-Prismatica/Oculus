# Requirements
* ```nodejs``` and ```npm```
* ```mongodb```
* ```python2```

For the ```pycrypto``` elements, ```python-dev``` or ```python-devel``` may be
required for native module compilationnstython.

# Running

Starting the node component:
```bash
$ npm install
$ node ./server.js
```

Starting the python component:
```bash
$ python2 -m virtualenv venv
$ ./venv/bin/pip2 install -r requirements.txt
$ ./venv/bin/python2 oculus.py
```