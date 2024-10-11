FROM node:latest AS build-web

WORKDIR /app/web

COPY ./web/package.json ./web/yarn.lock ./

RUN yarn install

COPY ./web ./

RUN yarn build

FROM python:3.12 AS build-venv

WORKDIR /app

RUN python -m pip install --upgrade poetry
RUN poetry config virtualenvs.create true
RUN poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock ./
RUN poetry install --only=main

FROM python:3.12-slim

WORKDIR /app

COPY --from=build-web /app/web/dist /app/web/dist

COPY --from=build-venv /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y curl

COPY ./resin /app/resin
COPY ./manage.py /app/manage.py

EXPOSE 8000

ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com

CMD bash -c " \
    python manage.py migrate --noinput && \
    python manage.py createsuperuser --noinput || true && \
    python manage.py collectstatic --noinput && \
    python manage.py runserver 0.0.0.0:8000"

HEALTHCHECK --interval=10s --timeout=3s CMD curl -f http://localhost:8000/health/ || exit 1
