# SHIP APP AI EVAL FRAMEWORK

An evaluation framework for the AI assistant in [Ship-app from QACart](https://github.com/QAcart-Premium/ship-app), built with DeepEval and pytest.

It talks to a running ShipTest instance over HTTP, sends it questions from a golden dataset, and scores the replies with an LLM judge.

This README covers setup and running only. What each metric checks is documented in the code under `support/metrics.py`.

## Requirements

- Python 3.14
- [uv](https://docs.astral.sh/uv/)
- A running [Ship-app](https://github.com/QAcart-Premium/ship-app) instance with its AI assistant enabled
- An OpenRouter API key for the judge model

Nothing else. The framework has no database and no server of its own.

## Setup

**1. Install dependencies**

```
uv sync
```

This creates `.venv` and installs the exact versions pinned in `uv.lock`.

**2. Create your environment file**

Create a file named `.env` in the project root:

```
SHIPTEST_BASE_URL=http://localhost:3000
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

`.env` is git-ignored and never committed.

**3. Get an API key**

Sign up and create a key at:

```
https://openrouter.ai/keys
```

Paste it into `.env` as the value of `OPENROUTER_API_KEY`.

**4. Start ShipTest**

Follow the ShipTest README, then check it is ready:

```
curl http://localhost:3000/api/agent/health
```

Expected:

```
{ "ok": true, "apiKeyConfigured": true }
```

## Running the tests

```
uv run python -m pytest tests/system-prompts-test.py --tb=short -v
uv run python -m pytest tests/rag-test.py --tb=short -v
uv run python -m pytest tests/agent-test.py --tb=short -v
```

Each golden becomes one test. A run makes one agent call and one judge evaluation per golden, so it takes about a minute and costs a few cents.

A failing test prints the metric name, the score, the threshold, and the judge's reason.

To run one group of tests inside a file, select it by name:

```
uv run python -m pytest tests/rag-test.py -k test_retriever --tb=short -v
```

Each run also writes one Markdown report per golden into `reports/`, named `PASSED_...` or `FAILED_...`.

## Configuration

Settings live in `support/config.py`.

| Setting | Value | Where it comes from |
|---|---|---|
| `BASE_URL` | `http://localhost:3000` | `SHIPTEST_BASE_URL` in `.env` |
| `OPENROUTER_API_KEY` | your key | `.env` |
| `SHIPTEST_EMAIL` | `jor@qacart.com` | constant in `config.py` |
| `SHIPTEST_PASSWORD` | `Test@1234` | constant in `config.py` |
| `JUDGE_MODEL` | `anthropic/claude-sonnet-5` | constant in `config.py` |

The login is one of the seed users from the ShipTest README. Each seed user is based in a different country, which changes which shipping rules apply, so changing the user changes what the tests exercise.

The judge is deliberately a different model from the one ShipTest uses for its agent.

## Project structure

| Path | What it holds |
|---|---|
| `data/` | Golden datasets as JSON |
| `models/` | Typed models for ShipTest's API responses |
| `scripts/` | Helpers, such as loading goldens from a JSON file and writing reports |
| `support/client.py` | Logs in to ShipTest and calls the agent and assistant endpoints |
| `support/config.py` | Settings and endpoint paths |
| `support/judge.py` | The judge model, through OpenRouter |
| `support/metrics.py` | The DeepEval metrics |
| `tests/` | The test files |
| `conftest.py` | Writes a report for each test after it runs |
| `reports/` | Generated reports, git-ignored |

## What is covered

| Area | Test file | Metrics |
|---|---|---|
| System prompt | `tests/system-prompts-test.py` | A GEval metric that checks replies against the formatting rules of the agent's system prompt |
| RAG generator | `tests/rag-test.py` | Faithfulness |
| RAG retriever | `tests/rag-test.py` | Contextual Relevancy, Contextual Recall, Contextual Precision |
| AI agent (tools) | `tests/agent-test.py` | Tool Correctness, Argument Correctness, Task Completion, plus custom GEval metrics for step efficiency and tool order |

## Purpose

Built for learning how to evaluate LLM applications, RAG pipelines and AI agents.
