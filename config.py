from os import environ as env

class TerminusGpsConfig:
    try:
        from dotenv import load_dotenv
    except ImportError:
        pass
    else:
        load_dotenv()

    DB_NAME = env.get("DB_NAME", None)
    DB_USER = env.get("DB_USER", None)
    DB_PASS = env.get("DB_PASS", None)
    DB_HOST = env.get("DB_HOST", None)
    DB_PORT = env.get("DB_PORT", None)
