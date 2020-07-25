FROM python:3.8-slim

RUN mkdir -p /app
WORKDIR /app
ADD . /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    locales-all \
    tzdata \
    python3-setuptools \
    python3-pip \
    python3-dev \
    python3-venv \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip && pip3 install pipenv && pip install uwsgi==2.0.18 && pip install --no-cache-dir -r requirements.txt


#CMD gunicorn jewels_shop.wsgi:application --bind 0.0.0.0:$PORT
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ./manage.py collectstatic
CMD uwsgi --http :8000 --wsgi-file jewels_shop/wsgi.py --master --process 4 --threads 2



#FROM python
#
#RUN mkdir -p /app
#WORKDIR /app
#ADD . /app
#
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    build-essential libffi-dev locales-all
#
#RUN pip install uwsgi==2.0.18
#RUN pip install --no-cache-dir -r requirements.txt
#
#RUN ["manage.py", "collectstatic"]
#CMD uwsgi --http :8000 --wsgi-file jewels_shop/wsgi.py --master --process 4 --threads 2



#FROM python
#
#
#RUN mkdir -p /usr/src/app/
#WORKDIR /usr/src/app/
#
#ADD . /usr/src/app/
#RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install uwsgi==2.0.18
#
##CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]