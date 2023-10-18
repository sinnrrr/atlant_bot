# # FROM --platform=linux/amd64 python:3.11-slim

# # RUN apt-get -y update && apt-get install --no-install-recommends -y wget
# # RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# # RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# # RUN pip install --no-cache-dir poetry

# # WORKDIR /app
# # COPY pyproject.toml poetry.lock ./
# # RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi
# # COPY . .

# # CMD ["python", "-m", "atlant_bot.main"]

# FROM zenika/alpine-chrome:with-chromedriver

# ENV PYTHONUNBUFFERED=1
# USER root

# RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
# RUN python3 -m ensurepip
# RUN pip3 install --no-cache --upgrade pip setuptools

# WORKDIR /app
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# USER chrome

# CMD ["python3", "-m", "atlant_bot.main"]

FROM --platform=linux/amd64 python:3.11-slim

RUN apt-get update && apt-get install -y chromium

RUN pip install --no-cache-dir poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi
COPY . .

CMD ["python", "-m", "atlant_bot.main"]
