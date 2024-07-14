from functools import wraps

from app.main.feedback.feedback_model import Feedback, FeedbackClassified
from app.main.openai.openai_service import FeedbackAnalyzer, OpenAi
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


class FeedbackDb:

    @staticmethod
    @session_scope
    def insere_registros_uhul(session, feedback, parsed_analysis):
        requested_features = []

        for feature in parsed_analysis["requested_features"]:
            feedback_classificado = FeedbackClassified(
                id_feedback=feedback.id,
                sentiment=parsed_analysis["sentiment"],
                code=feature["code"],
                reason=feature["reason"],
            )
            session.add(feedback_classificado)
            requested_features.append(
                {"code": feature["code"], "reason": feature["reason"]}
            )

        return {
            "id": str(feedback.guid),
            "sentiment": parsed_analysis["sentiment"].upper(),
            "requested_features": requested_features,
        }

    @staticmethod
    @session_scope
    def adicionar_feedback(session, item):
        feedback = Feedback(
            guid=item["id"],
            feedback=item["feedback"],
        )
        session.add(feedback)
        session.commit()
        session.refresh(feedback)

        # Analisar o feedback usando OpenAI
        service_open_ai = OpenAi()
        analise_feedback = service_open_ai.analyze_feedback(feedback.feedback)
        parsed_analysis = FeedbackAnalyzer.parse_analysis(analise_feedback)

        # Adicionar registros na tabela tb_feedbacks_classificados
        feedbacks_classifieds = FeedbackDb.insere_registros_uhul(
            feedback, parsed_analysis
        )

        return feedbacks_classifieds

    @staticmethod
    @session_scope
    def obter(session, id=None):
        if id:
            feedback = session.query(Feedback).filter_by(id=id).first()
            return feedback
        feedbacks = session.query(Feedback).all()
        return feedbacks
