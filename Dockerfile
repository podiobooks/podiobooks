FROM python:2.7
RUN apt-get update && \
    apt-get install -y apt-transport-https && \
    curl https://repo.varnish-cache.org/GPG-key.txt | apt-key add - && \
    echo "deb https://repo.varnish-cache.org/debian/ jessie varnish-4.0" >> /etc/apt/sources.list.d/varnish-cache.list && \
    apt-get update && \
    apt-get install -y varnish
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
# Copy the requirements and install them in order to cache this step for rebuilds
COPY podiobooks/requirements.txt /code/podiobooks/requirements.txt
COPY podiobooks/requirements_uwsgi.txt /code/podiobooks/requirements_uwsgi.txt
RUN pip install -r podiobooks/requirements_uwsgi.txt\