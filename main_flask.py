from enum import Enum
import logging
from pathlib import Path
from flask import Flask, request, abort, jsonify, redirect
from werkzeug.exceptions import HTTPException


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


static_path = str(Path(__file__).parent / "static")
app = Flask(__name__, static_url_path='', static_folder=static_path)


@app.errorhandler(Exception)
def handle_error(e):
    logger.exception(f"Got request: {request}\n\tdata: {request.data}\n\tform: {request.form}\n\targs: {request.args}")
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e), status=code), code


class ENDPOINTS(str, Enum):
    ROOT = "/"
    ROOT_HTML = "/index.html"
    LAMP = "/lamp"

    def __str__(self):
        return self.value


@app.route(ENDPOINTS.ROOT)
def root():
    return redirect(ENDPOINTS.ROOT_HTML)
