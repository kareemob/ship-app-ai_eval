from deepeval.metrics import ArgumentCorrectnessMetric, ContextualPrecisionMetric, GEval, FaithfulnessMetric, ContextualRelevancyMetric, ContextualRecallMetric, StepEfficiencyMetric, TaskCompletionMetric, ToolCorrectnessMetric
from deepeval.test_case import SingleTurnParams
from support.judge import get_judge

# CUSTOM METRICS (LLM)
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

# Generator metric (RAG)
def faithfulness():
    return FaithfulnessMetric(
    threshold = 0.75,
    model = get_judge()
)

# Retriever metrics (RAG)
def context_relevancy():
    return ContextualRelevancyMetric(
    threshold = 0.5,
    model = get_judge()
)

def context_recall():
    return ContextualRecallMetric(
    threshold = 0.5,
    model = get_judge()
)

def context_precision():
    return ContextualPrecisionMetric(
    threshold = 0.75,
    model = get_judge()
)

# Agent metrics
def tool_correctness():
    return ToolCorrectnessMetric(
        threshold = 1,
        model = get_judge()
    )

def argument_correctness():
    return ArgumentCorrectnessMetric(
    threshold = 1,
    model = get_judge()
)

def step_efficiency():
    return GEval(
    name="Step efficiency",
    evaluation_steps = [
    "Every tool call was needed to answer the input.",
    "No tool was called twice for the same purpose.",
    "The agent did not take extra steps before giving the answer.",
    ],
    evaluation_params = [SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT, SingleTurnParams.TOOLS_CALLED],
    threshold = 0.8,
    model = get_judge()
)

def task_completion():
    return TaskCompletionMetric(
    threshold = 0.8,
    model = get_judge()
)

def tool_order():
    return GEval(
    name="Tool order",
    evaluation_steps = [
    "Every tool in the expected tools appears in the tools called.",
    "The expected tools appear in the tools called in the same relative order as in the expected tools list.",
    "Extra tool calls before, between or after the expected tools are acceptable and do not lower the score.",
    "Calling an expected tool more than once is acceptable and does not lower the score.",
    ],
    evaluation_params = [SingleTurnParams.TOOLS_CALLED, SingleTurnParams.EXPECTED_TOOLS],
    threshold = 0.8,
    model = get_judge()
)