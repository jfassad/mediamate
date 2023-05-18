## Running locally

```bash
export TWILIO_ACCOUNT_SID=
export TWILIO_AUTH_TOKEN=
export OPENAI_API_KEY=
export SERPER_API_KEY=


python app.py
```

## Testing
```bash
MESSAGE="Hello"
TO_NUMBER="" # e.g. 552199999999
TWILIO_NUMBER="" # e.g. 14155238886
curl -v -X POST -d "Body=$MESSAGE&From=whatsapp%3A%2B$TO_NUMBER&To=whatsapp%3A%2B$TWILIO_NUMBER" http://localhost:5000/twilio/message
```
