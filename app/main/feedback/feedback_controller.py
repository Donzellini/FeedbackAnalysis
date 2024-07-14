from flask import request
from flask_restx import Namespace, Resource, fields

from app.main.feedback.feedback_service import FeedbackDb

api = Namespace("Feedback", description="")

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


@api.route("feedbacks")
class FeedbackPostController(Resource):
    @api.expect(feedback_model)
    @api.marshal_with(feedback_response_model, code=200)
    def post(self):
        feedback_data = request.json
        feedbacks_classifieds = FeedbackDb.adicionar_feedback(item=feedback_data)

        return feedbacks_classifieds, 201


@api.route("feedbacks/relatorio")
class FeedbackGetController(Resource):
    @api.response(200, "Busca realizada com sucesso")
    def get(self):
        feedbacks = FeedbackDb.obter()
        return [feedback.__dict__ for feedback in feedbacks], 200
