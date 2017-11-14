FROM alpine:3.6

RUN apk --update --no-cache add python3
RUN pip3 install bottle redis requests

WORKDIR /
COPY rdproxy.py /rdproxy.py
COPY docker-entrypoint.sh /docker-entrypoint.sh

ENV REDIS_HOST redis
ENV REDIS_PORT 6379
ENV REDIS_DB 0
ENV RDPROXY_PORT 80
ENV RDPROXY_DEBUG False
ENV RDPROXY_HOST 0.0.0.0

EXPOSE 80
CMD ["python3", "/rdproxy.py"]
