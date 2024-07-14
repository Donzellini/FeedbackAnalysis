from datetime import datetime, timedelta

from app.main.feedback.feedback_service import FeedbackService
from app.main.openai.openai_service import OpenAiService


def generate_weekly_report():
    one_week_ago = datetime.now() - timedelta(days=7)

    feedback_report = FeedbackService.generate_feedbacks_report(start_date=one_week_ago)

    percentage_positive = feedback_report["percentage_positive_feedbacks"]
    percentage_negative = 100 - float(percentage_positive[:-1])

    # Coletar principais funcionalidades e razões
    most_requested_features = feedback_report["most_requested_features"]
    features_info = [
        f"{feature['code']} ({feature['ocurrences']} ocorrências): "
        + ", ".join(reason["reason"] for reason in feature["reasons"])
        for feature in most_requested_features
    ]

    return percentage_positive, percentage_negative, features_info


def generate_email_body_weekly_report():
    percentage_positive, percentage_negative, features_info = generate_weekly_report()

    openai_service = OpenAiService()
    email_body = openai_service.generate_email_body_with_llm(
        percentage_positive, percentage_negative, features_info
    )

    return email_body
