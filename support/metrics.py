from deepeval.metrics import GEval, AnswerRelevancyMetric, HallucinationMetric
from deepeval.test_case import SingleTurnParams
from support.judge import get_judge


def system_prompt_compliance():
    return GEval(
    name="Chat style",
    evaluation_steps = [
    "Directly addresses what the input asked.",
    "Does not use Markdown tables.",
    "When it lists several items or values, uses short bullet points, one item per line. A reply with nothing to list does not violate this.",
    "When it reports a value, puts a label in bold with the value after it, for example **Total:** $82.00. A reply with no values to report does not violate this.",
    "Any money amount that appears is in USD. A reply with no money amounts does not violate this.",
    "Is concise: a direct answer plus the key numbers, not a long explanation.",
    ],
    evaluation_params = [SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
    threshold = 0.7,
    model = get_judge()
)