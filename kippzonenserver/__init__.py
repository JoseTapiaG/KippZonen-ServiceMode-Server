from flask import Flask
app = Flask(__name__)

import kippzonenserver.views
import kippzonenserver.context_processor