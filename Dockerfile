FROM python:3.11-alpine

WORKDIR /application

COPY requirements.txt /tmp/requirements.txt
COPY run.py /application
COPY app /application/app

RUN pip install -r /tmp/requirements.txt

ENV FLASK_APP=/application/run.py
ENV PYTHONPATH=/application/app

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
