FROM python:3.7

WORKDIR /srv/app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./app ./app
COPY ./tests ./tests
COPY ./pyproject.toml ./
COPY ./setup.cfg ./

CMD ["flask", "run"]
