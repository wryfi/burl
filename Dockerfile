FROM python:alpine3.7 as build
ARG uid=65432
RUN apk --no-cache add postgresql-dev gcc python3-dev musl-dev git
RUN mkdir -p /opt/burl
RUN addgroup -g ${uid} burl && adduser -D -u ${uid} -G burl -h /opt/burl burl
RUN pip install --no-cache-dir pipenv
ADD . /opt/burl/src
RUN chown -R burl:burl /opt/burl
USER ${uid}
WORKDIR /opt/burl/src
RUN pipenv lock -r > requirements.txt
RUN python setup.py bdist_wheel
RUN mkdir /opt/burl/pyscopg2
RUN PIP_NO_BINARY=psycopg2 pip install \
    --no-cache-dir --install-option="--prefix=/opt/burl/psycopg2" \
    $(grep psycopg2 requirements.txt)

FROM python:alpine3.7 as install
ARG uid=65432
RUN apk --no-cache add libpq
RUN mkdir -p /opt/burl
RUN addgroup -g ${uid} burl && adduser -D -u ${uid} -G burl -h /opt/burl burl
RUN chown -R burl:burl /opt/burl
RUN mkdir /root/psycopg2 /root/src
COPY --from=build /opt/burl/src/dist/*.whl /root/src
COPY --from=build /opt/burl/psycopg2 /root/psycopg2
RUN cp -R /root/psycopg2/* /usr/local && rm -rf /root/psycopg2
RUN pip install --no-cache-dir /root/src/*.whl && rm -rf /root/src
EXPOSE 8000/tcp
COPY ./docker_entrypoint.sh /usr/local/bin
USER ${uid}
ENTRYPOINT ["/usr/local/bin/docker_entrypoint.sh"]