FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv \
 && pipenv install --system

COPY . ./

CMD ["python", "./web.py"]
