import argparse
import logging

from flask import Flask, request, make_response
from incoming_message_handler import handle_message
from twilio_helper import create_twiml_response

app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.route('/twilio/message', methods=['POST'])
def twilio_message():
    try:
        content_type = request.headers.get('Content-Type')
        params = request.form
        request_body = request.get_data(as_text=True)

        _log_request(params, request_body, content_type)

        handle_message(params)

        return _send_response()
    except Exception as e:
        url = request.url
        logger.error(f"{e.__class__.__name__}: {str(e)}, URL: {url}")
        return send_error_response(str(e))


def _send_response(body=None):
    twiml_response_str = create_twiml_response(body)
    response = make_response(twiml_response_str, 200)
    response.headers['Content-Type'] = 'application/xml'
    return response


def _send_error_response(error_msg):
    twiml_response_str = create_twiml_response(f"Error: {error_msg}")
    response = make_response(twiml_response_str, 500)
    response.headers['Content-Type'] = 'application/xml'
    return response


def _log_request(params, request_body, content_type):
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
