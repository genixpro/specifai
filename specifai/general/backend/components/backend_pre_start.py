import logging
import os
from typing import Any

from pymongo.database import Database
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from specifai.general.backend.components.db import get_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = int(os.getenv("BACKEND_PRESTART_MAX_TRIES", 60 * 5))  # 5 minutes
wait_seconds = int(os.getenv("BACKEND_PRESTART_WAIT_SECONDS", 1))
reraise = os.getenv("BACKEND_PRESTART_RERAISE", "0") == "1"


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
    reraise=reraise,
)
def init(db: Database[dict[str, Any]]) -> None:
    try:
        db.command("ping")
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init(get_database())
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
