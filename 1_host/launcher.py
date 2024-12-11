from flask import Flask

# assign as build settings
from utils.combat import COMBAT_BUILDS_LIST

# assign as session settings
from utils.temps import SESSIONS_DICT_KEYS_AS_LIST

app = Flask(__name__)
if __name__ == "__main__":
  app.run(host="0.0.0.0")
