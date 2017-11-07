# rdproxy


**r**edis **d**riven **p**roxy


1. Just start `python rdproxy 8000`
2. e.g. in redis-cli `set u "http://127.0.0.1:8080/`
3. Browse `http://127.0.0.1:8000/u` and you get the content of your other app running on port 8080


# deps

* python 3
* `pip install bottle redis requests`
