# rdproxy


**r**edis **d**riven **p**roxy


1. Just start `python rdproxy 8000`
2. e.g. in redis-cli `set u "http://127.0.0.1:8080/`
3. Browse `http://127.0.0.1:8000/u` and you get the content of your other app running on port 8080


# deps

* python 3
* `pip install bottle redis requests`


# docker

1. make redis available
  * `docker run -d --name redis --net mynet -p 6379:6379 redis:alpine`
2. make some of your apps available
  * `docker run -d --name u1 --net mynet u:latest` 
  *  this one is a static page which listen on port 80, but not available from host
3. add route in redis
  * `set u "http://u1"`
  * don't forget `http://`! (`https` is not supported)
4. run rdproxy
  * `docker run -d --name rdproxy --net mynet -p 80:80 -e REDIS_HOST=redis rdproxy:latest`
5. enter in your browser `http://127.0.0.1/u/` and your docker server from step 2 will be available