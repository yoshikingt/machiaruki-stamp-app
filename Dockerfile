FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

#COPY requirements.txt ./
COPY Pipfile Pipfile.lock ./

# RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip install pipenv \
 && pipenv install --system

# COPY . .
COPY . ./

CMD ["python", "./web.py"]
