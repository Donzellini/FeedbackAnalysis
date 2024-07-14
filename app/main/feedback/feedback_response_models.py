from flask_restx import Api, Namespace, fields

api = Namespace("Feedback", description="API para análise qualitativa e quantitativa de feedbacks.")

feedback_post_model = api.model("FeedbackModel", {"id": fields.String, "feedback": fields.String})

requested_feature_model = api.model(
    "RequestedFeature", {"code": fields.String, "reason": fields.String}
)

feedback_post_response_model = api.model(
    "FeedbackResponseModel",
    {
        "id": fields.String,
        "sentiment": fields.String,
        "requested_features": fields.List(fields.Nested(requested_feature_model)),
    },
)

reason_model = api.model(
    "ReasonModel",
    {
        "reason": fields.String,
    },
)

requested_get_report_model = api.model(
    "RequestedFeatureModel",
    {
        "ocurrences": fields.Integer,
        "code": fields.String,
        "reasons": fields.List(fields.Nested(reason_model)),
    },
)

feedback_get_report_model = api.model(
    "FeedbackModel",
    {
        "id": fields.String,
        "feedback_user": fields.String,
        "sentiment": fields.String,
        "requested_features": fields.List(fields.Nested(requested_feature_model)),
    },
)

feedback_get_response_report_model = api.model(
    "FeedbackReportModel",
    {
        "percentage_positive_feedbacks": fields.String,
        "most_requested_features": fields.List(fields.Nested(requested_get_report_model)),
        "feedbacks": fields.List(fields.Nested(feedback_get_report_model)),
    },
)
