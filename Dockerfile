FROM python:3.10

ADD . / app /

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONPATH / app

#ENV SUBS=subscriber.py
#ENV SUBS=3000

EXPOSE 8000 3000


COPY . .

#ENTRYPOINT ["/run.sh"]