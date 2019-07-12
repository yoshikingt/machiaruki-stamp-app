FROM python:3

ENV PYTHONUNBUFFERED=1
ENV FLASK_RUN_HOST="0.0.0.0"
ENV FLASK_RUN_PORT="5000"

WORKDIR /usr/src/app

COPY . ./

RUN pip install pipenv \
 && pipenv install --system

CMD ["python", "./runserver.py"]
