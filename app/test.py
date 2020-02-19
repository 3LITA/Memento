import flask


app = flask.Flask(__name__)


@app.route('/')
def test() -> str:
    return 'Hello world!'


if __name__ == '__main__':
    app.run()
