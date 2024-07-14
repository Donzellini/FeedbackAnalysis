from flask import request, send_from_directory
from flask_restx import Resource

from app.main.feedback.feedback_response_models import FeedbackResponse, api
from app.main.feedback.feedback_service import FeedbackService

feedback_response = FeedbackResponse()


@api.route("feedbacks")
class FeedbackPostController(Resource):
    @api.expect(feedback_response.feedback_post_model)
    @api.marshal_with(feedback_response.feedback_post_response_model, code=200)
    def post(self):
        feedback_data = request.json
        feedbacks_classifieds = FeedbackService.add_feedback_analysis(item=feedback_data)
        return feedbacks_classifieds, 201


@api.route("feedbacks/relatorio")
class FeedbackGetController(Resource):
    @api.marshal_with(feedback_response.feedback_get_response_report_model, code=200)
    def get(self):
        feedbacks = FeedbackService.generate_feedbacks_report()
        return feedbacks, 200
