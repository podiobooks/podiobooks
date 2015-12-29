FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
# Copy the requirements and install them before copying in the whole tree in order to cache this step for rebuilds
COPY podiobooks/requirements.txt /code/podiobooks/requirements.txt
COPY podiobooks/requirements_uwsgi.txt /code/podiobooks/requirements_uwsgi.txt
RUN pip install -r podiobooks/requirements_prod.txt
COPY . /code/