import os
import time
import openai
from dotenv import load_dotenv
from slack_bolt import App
from slack_sdk.errors import SlackApiError

# Load environment variables from .env file
load_dotenv()

# Set up the Slack app and bot
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

# Set up the OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]


def is_bot_message(message):
    return (
        ("subtype" in message and message["subtype"] == "bot_message")
        or
        ("bot_id" in message)
        or
        ("bot_profile" in message)
    )



# Define a function to handle incoming messages
@app.event("message")
def handle_message(event, say):
    if "text" in event:
        # Get the message text and sender ID
        message_text = event["text"]
        message_channel = event["channel"]

        # Ignore messages sent by the bot itself. Ref: https://api.slack.com/events/message/bot_message
        if not is_bot_message(event):
            history = get_chat_history(channel_id=message_channel, latest_timestamp=event["ts"])

            history.append(
                {"role": "user", "content": message_text},
            )

            # Call the ChatGPT API to generate a response
            response = openai.ChatCompletion.create(
                model=os.environ["CHATGPT_MODEL"],
                messages=history,
                temperature=0,
            )

            # Parse message and fetch the text
            bot_response = response.choices[0].message.content

            # Send the response back to the user
            say(bot_response)


def get_chat_history(channel_id, latest_timestamp):
    chat_history = []

    try:
        # Call the conversations.history method using the WebClient
        # conversations.history returns the first 100 messages by default
        # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
        result = app.client.conversations_history(
            channel=channel_id,
            limit=40,
            oldest=str(time.time() - 7200),
            latest=latest_timestamp
        )

        conversation_history = result["messages"]

    except SlackApiError:
        conversation_history = []

    for message in conversation_history:
        if is_bot_message(message):
            role = "assistant"
        else:
            role = "user"

        chat_history.append({"role": role, "content": message["text"]})

    chat_history.reverse()

    return chat_history


# Start the app
if __name__ == "__main__":
    app.start(port=int(os.environ["CONTAINER_PORT"]))
