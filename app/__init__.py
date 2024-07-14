from flask import Blueprint, Flask, render_template
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from app.main.feedback.feedback_controller import api as feedback_ns

app = Flask(__name__, static_folder="app/static")
app.wsgi_app = ProxyFix(app.wsgi_app)

blueprint = Blueprint("api", __name__)
app.register_blueprint(blueprint)

api = Api(
    app,
    title="API Feedbacks",
    version="1.0",
    description="API para análise qualitativa e quantitativa de feedbacks.",
    prefix="/",
)

api.add_namespace(feedback_ns, path="/")


@app.route("/report")
def report():
    return render_template("report.html")
