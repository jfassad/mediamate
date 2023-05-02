# This file defines the IncomingMessageHandler class, which processes incoming messages.

import logging

from conversation_service import handle_conversation
from message_sender import send_message

logger = logging.getLogger(__name__)


def handle_message(params):

    body = params.get('Body')
    sender = params.get('From')
    recipient = params.get('To')

    response = handle_conversation(sender, body)

    # Swap sender and recipient because we want to send the response to the sender.
    sender, recipient = recipient, sender
    send_message(sender, recipient, response)


class IncomingMessageHandler:
    pass
