from collections import Counter
from functools import wraps

from app.main.feedback.feedback_model import Feedback, FeedbackClassified
from app.main.openai.openai_service import FeedbackAnalyzer, OpenAiService
from database import SessionLocal


def session_scope(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = SessionLocal()
        try:
            result = func(session, *args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    return wrapper


class FeedbackService:

    @staticmethod
    @session_scope
    def insert_registers(session, register, parsed_analysis):
        requested_features = []

        for feature in parsed_analysis["requested_features"]:
            feedback_classificado = FeedbackClassified(
                id_feedback=register.id,
                sentiment=parsed_analysis["sentiment"],
                code=feature["code"],
                reason=feature["reason"],
            )
            session.add(feedback_classificado)
            requested_features.append({"code": feature["code"], "reason": feature["reason"]})

        return {
            "id": str(register.guid),
            "sentiment": parsed_analysis["sentiment"].upper(),
            "requested_features": requested_features,
        }

    @staticmethod
    @session_scope
    def add_feedback_analysis(session, item):
        feedback = Feedback(
            guid=item["id"],
            feedback=item["feedback"],
        )
        session.add(feedback)
        session.commit()
        session.refresh(feedback)

        # Analisar o feedback usando OpenAI
        service_open_ai = OpenAiService()
        analise_feedback = service_open_ai.analyze_feedback(feedback.feedback)
        parsed_analysis = FeedbackAnalyzer.parse_analysis(analise_feedback)

        # Adicionar registros na tabela tb_feedbacks_classificados
        feedbacks_classifieds = FeedbackService.insert_registers(feedback, parsed_analysis)

        return feedbacks_classifieds

    @staticmethod
    @session_scope
    def generate_feedbacks_report(session):
        try:
            feedbacks = session.query(Feedback).all()

            # Calcular a porcentagem de feedbacks positivos
            total_feedbacks = len(feedbacks)
            positive_feedbacks = sum(
                1
                for feedback in feedbacks
                if any(
                    feature.sentiment.upper() == "POSITIVO"
                    for feature in feedback.feedback_classifieds
                )
            )
            percentage_positive_feedbacks = (
                (positive_feedbacks / total_feedbacks) * 100 if total_feedbacks > 0 else 0
            )

            # Encontrar as features mais pedidas com base no código que foi adicionado ao classificar o feedback
            features = session.query(FeedbackClassified).all()
            feature_counter = Counter(feature.code for feature in features)
            feature_reasons = {}
            for feature in features:
                if feature.code not in feature_reasons:
                    feature_reasons[feature.code] = []
                feature_reasons[feature.code].append({"reason": feature.reason})

            most_requested_features = [
                {"ocurrences": count, "code": code, "reasons": feature_reasons[code]}
                for code, count in feature_counter.most_common()
            ]

            response = {
                "percentage_positive_feedbacks": f"{percentage_positive_feedbacks:.2f}%",
                "most_requested_features": most_requested_features,
                "feedbacks": [],
            }

            # Adicionar feedbacks com suas requested_features
            for feedback in feedbacks:
                classified_features = [
                    {"code": feature.code, "reason": feature.reason}
                    for feature in session.query(FeedbackClassified)
                    .filter_by(id_feedback=feedback.id)
                    .all()
                ]
                response["feedbacks"].append(
                    {
                        "id": str(feedback.guid),
                        "feedback_user": feedback.feedback,
                        "sentiment": (
                            feedback.feedback_classifieds[0].sentiment.upper()
                            if feedback.feedback_classifieds
                            else ""
                        ),
                        "requested_features": classified_features,
                    }
                )

            return response
        finally:
            session.close()
