import os
import sys
from soundclaz import create_app


sys.path.insert(0, os.path.dirname(__file__))


def app(environ, start_response):
    app = create_app()
    return app
