# SHIP APP AI EVAL FRAMEWORK

An evaluation framework for the AI assistant in [ShipTest](https://github.com/QAcart-Premium/ship-app), built with DeepEval and pytest.

It talks to a running ShipTest instance over HTTP, sends it questions from a golden dataset, and scores the replies with an LLM judge.

This README covers setup and running only. What each metric checks is documented in the code under `support/metrics.py`.

## Requirements

- Python 3.14
- [uv](https://docs.astral.sh/uv/)
- A running ShipTest instance with its AI assistant enabled
- An OpenRouter API key for the judge model

The framework does not start ShipTest for you. Follow the ShipTest README first and confirm that `http://localhost:3000/api/agent/health` returns `"ok": true`.

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

OpenRouter is pay-as-you-go. The key in this project pays for the judge model only. ShipTest uses its own key from its own `.env`.

**4. Check the connection**

With ShipTest running:

```
uv run python -c "from support.client import chat; print(chat('How many shipments do I have?').reply)"
```

Expected: a short answer about the signed-in user's shipments.

## Running the tests

```
uv run python -m pytest tests/system-prompts-test.py --tb=short
```

Each golden becomes one test. A run makes one agent call and one judge evaluation per golden, so it takes about a minute and costs a few cents.

A failing test prints the metric name, the score, the threshold, and the judge's reason.

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
| `scripts/` | Helpers, such as loading goldens from a JSON file |
| `support/client.py` | Logs in to ShipTest and calls the agent's chat endpoint |
| `support/config.py` | Settings and endpoint paths |
| `support/judge.py` | The judge model, through OpenRouter |
| `support/metrics.py` | The DeepEval metrics |
| `tests/` | The test files |

## What is covered

| Area | Status |
|---|---|
| System prompt | A GEval metric that checks replies against the formatting rules of the agent's system prompt |
| RAG | Planned |
| AI agent (tools) | Planned |

## Troubleshooting

**`ConnectError` when a test starts**

ShipTest is not running, or `SHIPTEST_BASE_URL` points to the wrong address.

**`401` from the login call**

The email or password in `support/config.py` does not match a seed user. Re-seed ShipTest with `npm run reset`.

**`503` from the chat call**

ShipTest's own OpenRouter key is missing. That is set in ShipTest's `.env`, not in this project.

**`401` from the judge**

`OPENROUTER_API_KEY` is missing or wrong in this project's `.env`.

**`ModuleNotFoundError` for `scripts`, `support` or `models`**

Run the tests with `uv run python -m pytest` from the project root. That form puts the project root on the import path.

**`An Application Control policy has blocked this file (os error 4551)` on Windows**

Smart App Control is blocking a launcher in `.venv/Scripts`. Commands that start with `uv run python` are not affected.

**`SyntaxWarning: 'return' in a 'finally' block`**

This comes from DeepEval's own code on Python 3.14. It does not affect results.

## Notes

The goldens are written to put one rule of the system prompt under pressure each. An input that every reply would pass proves nothing.

Agent replies vary in wording between runs, even for the same question. The tests score meaning and rule compliance through the judge, not exact text.

## Purpose

Built for learning how to evaluate LLM applications, RAG pipelines and AI agents.
