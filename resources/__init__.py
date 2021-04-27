from pathlib import Path

_DIR = Path(__file__).parent

PATH_TEST_IMAGE1 = _DIR.joinpath("test-image.png")
PATH_TEST_IMAGE2 = _DIR.joinpath("test-image2.png")
PATH_DOTENV = _DIR.joinpath(".env")


def init_dotenv():
    """
    Init dotenv if it does not exist, otherwise load it
    """
    import shutil
    import dotenv

    path_dotenv_here = Path(".").joinpath(".env")
    if not path_dotenv_here.is_file():
        shutil.copy(PATH_DOTENV, path_dotenv_here)
    dotenv.load_dotenv()
