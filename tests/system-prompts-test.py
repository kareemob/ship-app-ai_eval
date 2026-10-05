from deepeval.test_case import LLMTestCase
from deepeval import  assert_test
from scripts.generate_datasets import generate_datasets_from_json
from support.client import chat
from support.metrics import system_prompt_compliance

import pytest

dataset = generate_datasets_from_json('./data/system_prompt_goldens.json', 'input')


@pytest.mark.parametrize("golden", dataset.goldens, ids=lambda golden: golden.name)
def test_system_prompt(golden):
    response = chat(golden.input)  # type: ignore
    answer = response.reply
    assert_test(
        test_case= LLMTestCase(
            input=golden.input,
              actual_output=answer
              ), # type: ignore
        metrics=[system_prompt_compliance()]
    )