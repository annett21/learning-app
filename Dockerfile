FROM python:3.11-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app
COPY pyproject.toml /app

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# Article: Dockerizing Python Poetry Applications
# https://medium.com/@harpalsahota/dockerizing-python-poetry-applications-1aa3acb76287
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev