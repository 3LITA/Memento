FROM python:3.8

WORKDIR /srv/app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./app ./app
COPY ./tests ./tests
COPY ./pyproject.toml ./
COPY ./setup.cfg ./

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
