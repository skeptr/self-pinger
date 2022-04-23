"""Простейший демонстрационный сервер."""


import json
import logging
import os

from fastapi import FastAPI, HTTPException, status

import uvicorn


class StupidCounter(object):

    def __init__(self) -> None:
        self._count = 0

    @property
    def value(self):
        return self._count

    def increment(self):
        self._count += 1


# Environment Variables
POSITIVE_DEBUG_ENV_VALUES = ("1", "true", "yes")

SELF_PINGER_NAME = os.getenv("SELF_PINGER_NAME") or "SelfPinger"

_debug_env = os.getenv("SELF_PINGER_DEBUG")
SELF_PINGER_DEBUG = False
if _debug_env and _debug_env.lower() in POSITIVE_DEBUG_ENV_VALUES:
    SELF_PINGER_DEBUG = True

try:
    SELF_PINGER_PERIOD = int(os.getenv("SELF_PINGER_PERIOD"))
except (TypeError, ValueError) as e:
    logging.error(e)
    SELF_PINGER_PERIOD = 0

# Logging
if SELF_PINGER_DEBUG:
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO
logging.basicConfig(
    format="%(asctime)s - %(levelname)-7s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=loglevel
)
logging.getLogger().propagate = False


# Application
ERR_MSG = "Да сколько можно уже?"
ERR_CODE = status.HTTP_403_FORBIDDEN
counter = StupidCounter()


def get_app_info_dict():
    loglevel = logging.getLogger().getEffectiveLevel()
    return {
        "config": {
            "SELF_PINGER_NAME": SELF_PINGER_NAME,
            "SELF_PINGER_DEBUG": SELF_PINGER_DEBUG,
            "SELF_PINGER_PERIOD": SELF_PINGER_PERIOD,
            "loglevel": logging.getLevelName(loglevel),
        },
        "requests_served": counter.value,
    }


app = FastAPI()
logging.info(f"Application {SELF_PINGER_NAME} started.")
logging.info(json.dumps(get_app_info_dict()))


# Endpoints
@app.get("/")
def home():
    return get_app_info_dict()


@app.get("/ping")
def self_ping():
    counter.increment()
    number = counter.value
    logging.debug(f"Ping #{number} begin")

    if (SELF_PINGER_PERIOD and
            number >= SELF_PINGER_PERIOD and
            number %  SELF_PINGER_PERIOD == 0):
        logging.error(f"Ping #{number} ERROR!")
        raise HTTPException(status_code=ERR_CODE, detail=ERR_MSG)

    logging.debug(f"Ping #{number} end")
    return {"alive": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
