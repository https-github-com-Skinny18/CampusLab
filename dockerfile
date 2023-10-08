FROM python:3.10

WORKDIR /app

RUN apt-get update && \
    apt-get install -qqy unzip libaio1 wget && \
    apt-get clean autoclean && \
    apt-get autoremove --yes && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

RUN apt-get update && apt-get install -y \
    libdbus-1-dev
RUN apt-get update && apt-get install -y \
    libcups2-dev
RUN apt-get update && apt-get install -y \
    libgirepository1.0-dev
RUN apt-get update && apt-get install -y \
    libldap2-dev libsasl2-dev
    
RUN mkdir /opt/oracle \
    && cd /opt/oracle

ADD ./ext_oracle/instantclient-basic-linux.x64-21.7.0.0.0dbru.zip /opt/oracle
ADD ./ext_oracle/instantclient-sdk-linux.x64-21.7.0.0.0dbru.zip /opt/oracle

RUN unzip /opt/oracle/instantclient-basic-linux.x64-21.7.0.0.0dbru.zip -d /opt/oracle \
    && unzip /opt/oracle/instantclient-sdk-linux.x64-21.7.0.0.0dbru.zip -d /opt/oracle \
    && ln -s /opt/oracle/instantclient_21_7 /opt/oracle/instantclient \
    && ln -s /opt/oracle/instantclient/lib* /usr/lib \
    && ln -s /opt/oracle/instantclient/sqlplus /usr/bin/sqlplus \
    && rm -rf /opt/oracle/*.zip

ENV LD_LIBRARY_PATH /opt/oracle/instantclient_21_7:${LD_LIBRARY_PATH}

COPY . . 

RUN /bin/sh -c python -m venv /app/iury 

RUN pip install --upgrade pip && \
    pip install setuptools_scm && \
    pip install -r requirements.txt && \
    pip install django psycopg2 && \
    pip install psycopg2 cx-Oracle


EXPOSE 9000

CMD ["/bin/bash", "-c", "source /app/iury/bin/activate && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]