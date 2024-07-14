from apscheduler.schedulers.background import BackgroundScheduler
from flask import Blueprint, Flask, render_template
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from app.main.email.email_service import send_email
from app.main.feedback.feedback_controller import api as feedback_ns
from app.main.feedback.feedback_jobs import generate_email_body_weekly_report
from app.main.openai.openai_service import OpenAiService

app = Flask(__name__, static_folder="app/static")
app.wsgi_app = ProxyFix(app.wsgi_app)

blueprint = Blueprint("api", __name__)
app.register_blueprint(blueprint)

# Configuração do servidor Flask
api = Api(
    app,
    title="API Feedbacks",
    version="1.0",
    description="API para análise qualitativa e quantitativa de feedbacks.",
    prefix="/",
)

api.add_namespace(feedback_ns, path="/")


# Rota preparada para acessar a página web contendo o relatório dos feedbacks e suas classificações
@app.route("/report")
def report():
    return render_template("report.html")


# Rota preparada para testar a rotina agendada de envio de e-mail
@app.route("/test-email-job")
def test_email():
    scheduled_job()
    return "Email enviado!"


# Configuração da rotina semanal de envio de e-mails, irá funcionar caso o servidor esteja rodando
def scheduled_job():
    email_body = generate_email_body_weekly_report()
    send_email(email_body)


scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, "interval", weeks=1)
scheduler.start()
