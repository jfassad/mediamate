# This file defines the IncomingMessageHandler class, which processes incoming messages.

import logging

from conversation_service import handle_conversation
from message_sender import send_message
from media_processing import DownloadService, AudioConverter

logger = logging.getLogger(__name__)


class IncomingMessageHandler:
    def __init__(self):
        self.download_service = DownloadService()
        self.converter = AudioConverter()

    def handle_message(self, params):
        body = params.get('Body')
        sender = params.get('From')
        recipient = params.get('To')
        mediaurl = params.get("MediaUrl0")

        if mediaurl:
            local_file_path = self.download_service.download_media_file(mediaurl)
            logger.info(f"Downloaded file path: {local_file_path}")
            output_mp3_file = self.converter.convert_to_mp3(local_file_path)
            logger.info(f"Output MP3 file: {output_mp3_file}")

        response = handle_conversation(sender, body)

        # Swap sender and recipient because we want to send the response to the sender.
        sender, recipient = recipient, sender
        send_message(sender, recipient, response)
