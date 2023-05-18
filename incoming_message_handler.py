import logging

from conversation_service import handle_conversation
from twilio_helper import send_message
from media_processing import transcribe_audio

logger = logging.getLogger(__name__)


def _handle_media_message(url):
    return transcribe_audio(url)


def _handle_text_message(sender, body):
    response = handle_conversation(sender, body)
    return response


def handle_message(params):
    body = params.get('Body')
    sender = params.get('From')
    recipient = params.get('To')
    url = params.get("MediaUrl0")

    if url:
        logger.debug(f"Processsing media message: {url}")
        response = _handle_media_message(url)
    else:
        logger.debug("Processsing text message")
        response = _handle_text_message(sender, body)

    # Swap sender and recipient because we want to send the response to the sender.
    sender, recipient = recipient, sender
    send_message(sender, recipient, response)
