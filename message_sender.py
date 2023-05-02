# This file defines the MessageSender class, which sends messages using the Twilio API.

import logging
from time import sleep
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 1600
MESSAGE_DELAY_MS = 500  # delay between messages in milliseconds


def send_message(sender, recipient, body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message_parts = split_message(body, MAX_MESSAGE_LENGTH)
    has_multiple_parts = len(message_parts) > 1

    for i, message_part in enumerate(message_parts):
        if has_multiple_parts:
            message_part = f"({i + 1}/{len(message_parts)}) {message_part}"
        send_single_message(client, sender, recipient, message_part, i, len(message_parts))


def send_single_message(client, sender, recipient, message_part, index, total_parts):
    try:
        message = client.messages.create(
            body=message_part,
            from_=sender,
            to=recipient
        )
        logger.debug(f"Message sent with sid {message.sid}")

        if index < total_parts - 1:
            sleep(MESSAGE_DELAY_MS / 1000)
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        raise e


def split_message(body, max_length):
    message_parts = []
    body_length = len(body)
    start_index = 0

    while start_index < body_length:
        end_index = min(start_index + max_length - 10, body_length)
        end_index = find_last_boundary(body, start_index, end_index)
        message_parts.append(body[start_index:end_index])
        start_index = end_index

    return message_parts


def find_last_boundary(body, start_index, end_index):
    if end_index >= len(body):
        return end_index

    punctuation = ".,!?:;"
    last_boundary_index = -1

    for punct in punctuation:
        last_index = body.rfind(punct, start_index, end_index)
        last_boundary_index = max(last_boundary_index, last_index)

    return last_boundary_index + 1 if last_boundary_index != -1 and last_boundary_index >= start_index else end_index


class MessageSender:
    pass

