# This file defines the Flask application and its endpoints.

import argparse
import logging

from flask import Flask, request, make_response
from incoming_message_handler import IncomingMessageHandler

app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.route('/twilio/message', methods=['POST'])
def receive_message():
    content_type = request.headers.get('Content-Type')
    params = request.form
    request_body = request.get_data(as_text=True)

    log_request(params, request_body, content_type)

    handler = IncomingMessageHandler()
    handler.handle_message(params)

    return send_response()


def send_response():
    response = make_response('', 200)
    response.headers['Content-Type'] = 'text/plain'
    return response


@app.errorhandler(Exception)
def handle_exception(e):
    url = request.url
    logger.error(f"{e.__class__.__name__}: {str(e)}, URL: {url}")
    return make_response('Internal Server Error', 500)


def log_request(params, request_body, content_type):
    logger.debug("Received parameters:")
    for key, value in params.items():
        logger.debug(f"Parameter: {key} = {value}")

    logger.debug(f"Received request body: {request_body}")
    logger.debug(f"Received content-type: {content_type}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Flask app with optional port binding.")
    parser.add_argument('--port', type=int, default=5000, help="Port number to bind the server to. Default is 5000.")
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port, debug=True)
