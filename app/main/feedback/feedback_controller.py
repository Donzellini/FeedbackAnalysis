from flask import request
from flask_restx import Resource

from app.main.feedback.feedback_response_models import (
    api,
    feedback_get_response_report_model,
    feedback_post_model,
    feedback_post_response_model,
)
from app.main.feedback.feedback_service import FeedbackService


@api.route("feedbacks")
class FeedbackPostController(Resource):
    @api.expect(feedback_post_model)
    @api.marshal_with(feedback_post_response_model, code=200)
    def post(self):
        feedback_data = request.json
        feedbacks_classifieds = FeedbackService.add_feedback_analysis(item=feedback_data)
        return feedbacks_classifieds, 201


@api.route("feedbacks/relatorio")
class FeedbackGetController(Resource):
    @api.marshal_with(feedback_get_response_report_model, code=200)
    def get(self):
        feedbacks = FeedbackService.generate_feedbacks_report()
        return feedbacks, 200
