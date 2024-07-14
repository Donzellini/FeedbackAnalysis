from collections import Counter


class FeedbackFunctions:

    @staticmethod
    def calculate_percentage_positive_feedbacks(feedbacks):
        total_feedbacks = len(feedbacks)
        positive_feedbacks = sum(
            1
            for feedback in feedbacks
            if any(
                feature.sentiment.upper() == "POSITIVO" for feature in feedback.feedback_classifieds
            )
        )
        percentage_positive_feedbacks = (
            (positive_feedbacks / total_feedbacks) * 100 if total_feedbacks > 0 else 0
        )

        return percentage_positive_feedbacks

    @staticmethod
    def find_most_requested_features(features):
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

        return most_requested_features
