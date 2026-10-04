from deepeval.models import OpenRouterModel
from support.config import JUDGE_MODEL, OPENROUTER_API_KEY


def get_judge():
    return OpenRouterModel(
        model=JUDGE_MODEL
    )