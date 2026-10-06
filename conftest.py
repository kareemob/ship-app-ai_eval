import pytest
from scripts.save_report import save_report


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    data = getattr(item, "report_data", None)
    if data is None:
        return

    golden, answer, items = data
    if report.passed:
        save_report(item.originalname, golden, answer, items, "PASSED")
    else:
        save_report(item.originalname, golden, answer, items, "FAILED", str(call.excinfo.value))