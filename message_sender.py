# This file defines the MessageSender class, which sends messages using the Twilio API.

import logging

from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

logger = logging.getLogger(__name__)

class MessageSender:
    @staticmethod
    def send_message(sender, recipient, body):
        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            message = client.messages.create(
                body=body,
                from_=sender,
                to=recipient
            )

            logger.info(message.sid)
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            raise e
