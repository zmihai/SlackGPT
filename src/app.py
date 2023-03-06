import os
import slack_bolt
import openai

from dotenv import load_dotenv
from slack_bolt import App

# Load environment variables from .env file
load_dotenv()

# Set up the Slack app and bot
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

# Set up the OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]


# Define a function to handle incoming messages
@app.event("message")
def handle_message(event, say):
    if "text" in event:
        # Get the message text and sender ID
        message_text = event["text"]

        # Ignore messages sent by the bot itself. Ref: https://api.slack.com/events/message/bot_message
        if ("subtype" not in event) or (event["subtype"] != "bot_message"):
            # Call the ChatGPT API to generate a response
            response = openai.ChatCompletion.create(
                model=os.environ["CHATGPT_MODEL"],
                messages=[
                    {"role": "user", "content": message_text},
                ],
                temperature=0,
            )

            # Parse message and fetch the text
            bot_response = response.choices[0].message.content

            # Send the response back to the user
            say(bot_response)


# Start the app
if __name__ == "__main__":
    app.start(port=int(os.environ["CONTAINER_PORT"]))
