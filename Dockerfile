FROM python:3.10-alpine as build
ARG uid=65432
RUN apk --no-cache add postgresql-dev gcc musl-dev git
RUN mkdir -p /opt/burl \
    && addgroup -g ${uid} burl \
    && adduser -D -u ${uid} -G burl -h /opt/burl burl \
    && pip install --no-cache-dir -U setuptools \
    && pip install --no-cache-dir build pipenv
ADD . /opt/burl/src
RUN chown -R burl:burl /opt/burl
USER ${uid}
WORKDIR /opt/burl/src
RUN rm -rf /opt/burl/src/dist/* /opt/burl/psycopg2 \
    && [[ -f requirements.txt ]] || pipenv lock -r > requirements.txt \
    && python setup.py bdist_wheel \
    && mkdir /opt/burl/pyscopg2 \
    && PIP_NO_BINARY=psycopg2 pip install \
    --no-cache-dir --prefix=/opt/burl/psycopg2 \
    $(grep psycopg2 requirements.txt)

FROM python:3.10-alpine as install
ARG uid=65432
RUN apk --no-cache add libpq
RUN mkdir -p /opt/burl /root/psycopg2 /root/src \
    && addgroup -g ${uid} burl && adduser -D -u ${uid} -G burl -h /opt/burl burl \
    && chown -R burl:burl /opt/burl \
    && pip install -U setuptools
COPY --from=build /opt/burl/src/dist/*.whl /root/src/
COPY --from=build /opt/burl/psycopg2 /root/psycopg2
RUN cp -R /root/psycopg2/* /usr/local && rm -rf /root/psycopg2 \
    && pip install --no-cache-dir /root/src/*.whl && rm -rf /root/src
EXPOSE 8000/tcp
COPY ./docker_entrypoint.sh /usr/local/bin
USER ${uid}
ENTRYPOINT ["/usr/local/bin/docker_entrypoint.sh"]
