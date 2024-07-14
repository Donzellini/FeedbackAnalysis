from flask import Blueprint, Flask
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from app.main.feedback.feedback_controller import api as home_ns
from database import Base, engine

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
blueprint = Blueprint("api", __name__)
app.register_blueprint(blueprint)

api = Api(
    app,
    title="API Feedbacks",
    version="1.0",
    description="API para controle de feedbacks",
    prefix="/api",
)

api.add_namespace(home_ns, path="/")
