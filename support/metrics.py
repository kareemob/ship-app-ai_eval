from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams
from support.judge import get_judge


def system_prompt_compliance():
    return GEval(
    name="Chat style",
    evaluation_steps = [
    "Does not use Markdown tables.",
    "Uses short bullet points, one item per line.",
    "Puts a label in bold with the value after it, for example **Total:** $82.00.",
    "All money amounts are in USD.",
    "Is concise: a direct answer plus the key numbers, not a long explanation.",
    ],
    evaluation_params = [SingleTurnParams.ACTUAL_OUTPUT],
    threshold = 0.7,
    model = get_judge()
)