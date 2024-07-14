from flask import request
from flask_restx import Namespace, Resource, fields

from app.main.feedback.feedback_service import FeedbackService

api = Namespace("Feedback", description="API para análise qualitativa e quantitativa de feedbacks.")

feedback_model = api.model("FeedbackModel", {"id": fields.String, "feedback": fields.String})

requested_feature_model = api.model(
    "RequestedFeature", {"code": fields.String, "reason": fields.String}
)

feedback_response_model = api.model(
    "FeedbackResponseModel",
    {
        "id": fields.String,
        "sentiment": fields.String,
        "requested_features": fields.List(fields.Nested(requested_feature_model)),
    },
)

feedback_report_model = api.model(
    "FeedbackReportModel",
    {
        "percentage_positive_feedbacks": fields.String,
        "most_requested_features": fields.List(fields.Nested(requested_feature_model)),
        "feedbacks": fields.List(fields.Nested(feedback_model)),
    },
)


@api.route("feedbacks")
class FeedbackPostController(Resource):
    @api.expect(feedback_model)
    @api.marshal_with(feedback_response_model, code=200)
    def post(self):
        feedback_data = request.json
        feedbacks_classifieds = FeedbackService.add_feedback_analysis(item=feedback_data)

        return feedbacks_classifieds, 201


@api.route("feedbacks/relatorio")
class FeedbackGetController(Resource):
    @api.marshal_with(feedback_report_model, code=200)
    def get(self):
        feedbacks = FeedbackService.generate_feedbacks_report()
        return feedbacks, 200
