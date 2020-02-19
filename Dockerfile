FROM python:3.7

WORKDIR /srv/app
RUN pip install -r requirements.txt

COPY ./app ./app
COPY ./pyproject.toml ./
COPY ./setup.cfg ./

CMD ["flask", "run"]
