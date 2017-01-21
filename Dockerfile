FROM pypy:2-5.6.0

RUN mkdir -p /pypy
RUN set -x \
    && curl -SL "https://bitbucket.org/pypy/pypy/downloads/pypy2-v5.6.0-src.tar.bz2" \
        | tar -xjC /pypy --strip-components=1

RUN mkdir -p /src
WORKDIR /src

ADD requirements.txt /src
RUN pip install -r requirements.txt

CMD ["pypy", "/src/pybibim.py", "/testcode/helloworld.bibim"]