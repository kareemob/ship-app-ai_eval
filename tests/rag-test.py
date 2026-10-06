from deepeval.test_case import LLMTestCase
from deepeval import  assert_test
from scripts.generate_datasets import generate_datasets_from_json
from support.client import ask, search
from support.metrics import context_precision, context_recall, context_relevancy, faithfulness

import pytest

dataset = generate_datasets_from_json('./data/rag_goldens.json', 'input')


# @pytest.mark.parametrize("golden", dataset.goldens, ids=lambda golden: golden.name)
# def test_generator(golden, request):
#     answer = ask(golden.input).answer  # type: ignore
#     chunks = search(golden.input).results  # type: ignore
#     request.node.report_data = (golden, answer, chunks)
#     assert_test(
#         test_case= LLMTestCase(
#             input=golden.input,
#               actual_output=answer,
#               retrieval_context=[chunk.content for chunk in chunks]
#               ), # type: ignore
#         metrics=[faithfulness()]
#     )

# @pytest.mark.parametrize("golden", dataset.goldens, ids=lambda golden: golden.name)
# def test_retriever(golden, request):
#     chunks = search(golden.input).results  # type: ignore
#     request.node.report_data = (golden, "(not generated: retriever test)", chunks)
#     assert_test(
#         test_case= LLMTestCase(
#             input=golden.input,
#               retrieval_context=[chunk.content for chunk in chunks]
#               ), # type: ignore
#         metrics=[context_relevancy()]
#     )    

# @pytest.mark.parametrize("golden", dataset.goldens, ids=lambda golden: golden.name)
# def test_retriever(golden, request):
#     chunks = search(golden.input).results  # type: ignore
#     request.node.report_data = (golden, "(not generated: retriever test)", chunks)
#     assert_test(
#         test_case= LLMTestCase(
#             expected_output=golden.expected_output,
#             input=golden.input,
#               retrieval_context=[chunk.content for chunk in chunks]
#               ), # type: ignore
#         metrics=[context_recall()]
#     )   

@pytest.mark.parametrize("golden", dataset.goldens, ids=lambda golden: golden.name)
def test_retriever(golden, request):
    chunks = search(golden.input).results  # type: ignore
    request.node.report_data = (golden, "(not generated: retriever test)", chunks)
    assert_test(
        test_case= LLMTestCase(
            expected_output=golden.expected_output,
            input=golden.input,
              retrieval_context=[chunk.content for chunk in chunks]
              ), # type: ignore
        metrics=[context_precision()]
    )   