from flask import Flask

from pandora.views import pandora_page
from settings import settings

app = Flask(__name__)
app.register_blueprint(pandora_page)
app.config["SECRET_KEY"] = settings["SECRET_KEY"]


if __name__ == "__main__":
    app.run(debug=True)
