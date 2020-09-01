from app.server import web


def serve():
    web.run(debug=False)


if __name__ == '__main__':
    serve()
