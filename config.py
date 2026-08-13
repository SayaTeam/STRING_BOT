from os import getenv
from dotenv import load_dotenv

load_dotenv()

def _get_int(var_name: str, default: int = 0) -> int:
    val = getenv(var_name)
    if not val:
        return default
    try:
        return int(val.strip())
    except (ValueError, AttributeError):
        return default

#❖________①_______❖_______#
API_ID = _get_int("API_ID")

#❖________②_______❖_______#
API_HASH = getenv("API_HASH", None)

#❖________③_______❖_______#
BOT_TOKEN = getenv("BOT_TOKEN", None)

#❖________④_______❖_______#
OWNER_ID = _get_int("OWNER_ID")

#❖________⑤_______❖_______#
MONGO_DB_URI = getenv("MONGO_DB_URI", getenv("MONGO_URL", None))

#❖________⑥_______❖_______#
MUST_JOIN = getenv("MUST_JOIN", None)
