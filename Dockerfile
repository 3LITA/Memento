FROM python:3.8 AS base

WORKDIR /srv/app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 5000

FROM base AS app

COPY ./app ./app
COPY ./pyproject.toml ./setup.cfg ./logging-config.yaml ./babel.cfg ./
RUN pybabel compile -d app/i18n
CMD ["gunicorn", "-k", "sync", "-w", "5", "-b", "0.0.0.0:5000", "app.server:web"]

FROM app AS dev

COPY ./ ./
