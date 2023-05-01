# This file defines the IncomingMessageHandler class, which processes incoming messages.

import logging

from conversation_service import ConversationService
from message_sender import MessageSender

logger = logging.getLogger(__name__)

class IncomingMessageHandler:
    @staticmethod
    def handle_message(params):

        body = params.get('Body')
        sender = params.get('From')
        recipient = params.get('To')

        response = ConversationService.handle_message(body)
        MessageSender.send_message(recipient, sender, response)
