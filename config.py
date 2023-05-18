import os
import logging

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']

# OpenAI API key from https://platform.openai.com/account/api-keys
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# Serper API key from https://serper.dev/api-key
SERPER_API_KEY = os.environ["SERPER_API_KEY"]


# Set log level to INFO
logging.basicConfig(level=logging.INFO)

# Disable Flask access logs
flask_logger = logging.getLogger('werkzeug')
flask_logger.disabled = True

# Disable Twilio client logs
twilio_logger = logging.getLogger('twilio.http_client')
twilio_logger.setLevel(logging.WARNING)

# Set OpenAI log level to INFO
openai_logger = logging.getLogger('openai')
openai_logger.setLevel(logging.DEBUG)
