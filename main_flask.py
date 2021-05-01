import app.app as app
from app.settings import Globals
import logging
import sys
from webserver.server.routes import app as flask_app, socketio, ENDPOINTS
import resources
from resources.util import get_env
resources.init_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# The number of NeoPixels
PIXEL_COUNT = get_env("RPI_LED_SERVER_PIXEL_COUNT", 50, int)
NEW_SESSION = get_env("RPI_LED_SERVER_NEW_SESSION", False, bool)
PORT = get_env("RPI_LED_SERVER_PORT", 5000, int)
HOST = get_env("RPI_LED_SERVER_HOST", "0.0.0.0")


if not NEW_SESSION:
    try:
        Globals.load()
    except FileNotFoundError:
        logger.info("No previous led session file found")


@flask_app.before_first_request
def start():
    app.start(num_pixels=PIXEL_COUNT)


@flask_app.route(ENDPOINTS.SHUTDOWN, methods=("POST",))
def shutdown():
    app.stop()


def main():
    print("Starting app", flush=True, file=sys.stderr)
    if not NEW_SESSION:
        try:
            Globals.load()
        except FileNotFoundError:
            logger.info("No previous led session file found")

    socketio.run(HOST, port=PORT, debug=True)


if __name__ == "__main__":
    main()
