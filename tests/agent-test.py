from deepeval.test_case import LLMTestCase, ToolCall
from deepeval import  assert_test
from scripts.generate_datasets import generate_datasets_from_json
from support.client import chat
from support.metrics import  tool_correctness, argument_correctness, task_completion, step_efficiency, tool_order

import pytest

dataset = generate_datasets_from_json('./data/agent_goldens.json', 'input')

# @pytest.mark.parametrize("golden", dataset.goldens, ids=lambda golden: golden.name)
# def test_agent_uses_correct_tool(golden, request):
#     response = chat(golden.input)  # type: ignore
#     request.node.report_data = (golden, response.reply, response.tool_calls)
#     assert_test(
#         test_case= LLMTestCase(
#             input=golden.input,
#             actual_output=response.reply,
#             tools_called=[ToolCall(name=tool.name, input_parameters=tool.args, output=tool.result)
#                 for tool in response.tool_calls], # type: ignore
#             expected_tools=golden.expected_tools
#               ), # type: ignore
#         metrics=[tool_correctness(), argument_correctness()]
#     )    

# @pytest.mark.parametrize("golden", dataset.goldens, ids=lambda golden: golden.name)
# def test_agent_steps_are_efficient(golden, request):
#     if golden.name == "save_draft_shipment":
#      pytest.skip("needs the form to resolve the sender; not an efficiency case")
#     response = chat(golden.input)  # type: ignore
#     request.node.report_data = (golden, response.reply, response.tool_calls)
#     assert_test(
#         test_case= LLMTestCase(
#             input=golden.input,
#             actual_output=response.reply,
#             tools_called = [
#                 ToolCall(name=tool.name, input_parameters=tool.args, output=tool.result)
#                 for tool in response.tool_calls
#             ]
#               ), # type: ignore
#         metrics=[step_efficiency()]
#     )
# task_dataset = generate_datasets_from_json('./data/agent_task_goldens.json', 'input')   

# @pytest.mark.parametrize("golden", task_dataset.goldens, ids=lambda golden: golden.name)
# def test_agent_completes_task(golden, request):
#     response = chat(golden.input)  # type: ignore
#     request.node.report_data = (golden, response.reply, response.tool_calls)
#     assert_test(
#         test_case= LLMTestCase(
#             input=golden.input,
#             actual_output=response.reply,
#             tools_called = [
#                 ToolCall(name=tool.name, input_parameters=tool.args, output=tool.result)
#                 for tool in response.tool_calls
#             ]
#               ), # type: ignore
#         metrics=[task_completion()]
#     )

@pytest.mark.parametrize("golden", dataset.goldens, ids=lambda golden: golden.name)
def test_agent_calls_tools_in_order(golden, request):
    if len(golden.expected_tools) < 2:
        pytest.skip("order only matters with two or more expected tools")
    response = chat(golden.input)  # type: ignore
    request.node.report_data = (golden, response.reply, response.tool_calls)
    assert_test(
        test_case= LLMTestCase(
            input=golden.input,
            actual_output=response.reply,
            tools_called = [
                ToolCall(name=tool.name, input_parameters=tool.args, output=tool.result)
                for tool in response.tool_calls
            ],
            expected_tools=golden.expected_tools
              ), # type: ignore
        metrics=[tool_order()]
    )    
