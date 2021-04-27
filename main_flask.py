import os
import app.app as app
from app.settings import Globals
import logging
import sys
import dotenv
dotenv.load_dotenv()
from webserver.server.routes import app as flask_app


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# The number of NeoPixels
pixel_count_str = os.getenv("RPI_LED_SERVER_PIXEL_COUNT", 50)
try:
    PIXEL_COUNT = int(pixel_count_str)
except TypeError:
    logger.error(f"Could not interpret RPI_LED_SERVER_PIXEL_COUNT ({pixel_count_str}) as a number. Using default value.")
    PIXEL_COUNT = 50
NEW_SESSION = os.getenv("RPI_LED_SERVER_NEW_SESSION", False)
PORT = os.getenv("RPI_LED_SERVER_NEW_SESSION", False)
HOST = os.getenv("RPI_LED_SERVER_HOST", "0.0.0.0")


if not NEW_SESSION:
    try:
        Globals.load()
    except FileNotFoundError:
        logger.info("No previous led session file found")


@flask_app.before_first_request
def start():
    app.start(num_pixels=PIXEL_COUNT)


@flask_app.route("/shutdown", methods=("POST",))
def shutdown():
    app.stop()


def main():
    print("Starting app", flush=True, file=sys.stderr)
    if not NEW_SESSION:
        try:
            Globals.load()
        except FileNotFoundError:
            logger.info("No previous led session file found")

    flask_app.run(HOST, port=PORT, debug=True)


if __name__ == "__main__":
    main()
