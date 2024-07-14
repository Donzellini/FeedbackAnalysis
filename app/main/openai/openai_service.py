import re

from openai import OpenAI
from unidecode import unidecode

from config import OPENAI_KEY

client = OpenAI(api_key=OPENAI_KEY)


class OpenAiService:

    @staticmethod
    def analyze_feedback(feedback):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente especializado em análise de feedback.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Analise o seguinte feedback e, por favor, forneça a resposta na seguinte estrutura:\n"
                        f"Sentimento: [positivo, negativo, inconclusivo]\n"
                        f"Possíveis melhorias:\n- [detalhe da melhoria 1]\n- [detalhe da melhoria 2]\n\n"
                        f"Feedback: {feedback}"
                    ),
                },
            ],
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()

    @staticmethod
    def generate_code_for_improvement(reason):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um gerador de código."},
                {
                    "role": "user",
                    "content": (
                        f"Baseado na seguinte melhoria, identifique DUAS palavras significativas para "
                        f"identificação da melhoria e retorne no formato: Palavras Significativas: [palavra1, palavra2]: {reason}"
                    ),
                },
            ],
            max_tokens=20,
        )
        return response.choices[0].message.content.strip()


class FeedbackAnalyzer:
    @staticmethod
    def parse_analysis(analysis):
        sentiment = None
        requested_features = []

        sentiment_match = re.search(
            r"Sentimento:\s*(Positivo|Negativo|Inconclusivo)",
            analysis,
            re.IGNORECASE,
        )
        if sentiment_match:
            sentiment = sentiment_match.group(1).upper()

        improvements_match = re.search(
            r"Possíveis melhorias:\s*((?:\d+\.\s*.*|-\s*.*(?:\n\s*|$))*)",
            analysis,
            re.IGNORECASE | re.DOTALL,
        )
        if improvements_match:
            improvements = improvements_match.group(1).strip().split("\n")
            for improvement in improvements:
                improvement = improvement.strip()
                if improvement.startswith(("-", "1.")):
                    reason = (
                        improvement.split(". ", 1)[0].strip()
                        if "." in improvement
                        else improvement[2:].strip()
                    )
                    code = FeedbackAnalyzer.generate_code(reason)
                    requested_features.append({"code": code, "reason": reason})

        return {
            "sentiment": sentiment,
            "requested_features": requested_features,
        }

    @staticmethod
    def generate_code(reason):
        suggested_code = OpenAiService.generate_code_for_improvement(reason)

        match = re.search(r"Palavras Significativas:\s*\[(\w+),\s*(\w+)]", suggested_code)
        if match:
            word1 = unidecode(re.sub(r"\W+", "", match.group(1))).upper()
            word2 = unidecode(re.sub(r"\W+", "", match.group(2))).upper()
            return f"{word1}_{word2}"
        else:
            return "DEFAULT_CODE"
