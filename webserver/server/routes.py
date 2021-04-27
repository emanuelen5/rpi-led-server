from enum import Enum
from pathlib import Path
from util import cycle_enum
from app.settings import Globals
from flask import Flask, request, jsonify, redirect
from werkzeug.exceptions import HTTPException
import logging

logger = logging.getLogger(__name__)

static_path = str(Path(__file__).parent.joinpath("../.build"))
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
    SETTINGS = "/settings"

    def __str__(self):
        return self.value


@app.route(ENDPOINTS.ROOT)
def root():
    return redirect(ENDPOINTS.ROOT_HTML)


@app.route(ENDPOINTS.SETTINGS)
def get_settings():
    Globals.main_mode = cycle_enum(Globals.main_mode)
    return {
        "led_settings": Globals.led_settings,
        "main_mode": Globals.main_mode.name,
        "select_mode": Globals.select_mode.name,
        "led_mode": Globals.led_mode.name
    }
