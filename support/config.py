import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('SHIPTEST_BASE_URL')
SHIPTEST_LOGIN_URL = '/api/auth/login'
SHIPTEST_CHAT_URL = '/api/agent/chat'

SHIPTEST_EMAIL = 'jor@qacart.com'
SHIPTEST_PASSWORD = 'Test@1234'

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
JUDGE_MODEL = 'anthropic/claude-sonnet-5'