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
        sender_id = event["user"]

        # Ignore messages sent by the bot itself
        if sender_id != app.client.auth_test()["user_id"]:
            # Call the ChatGPT API to generate a response
            response = openai.Completion.create( engine="davinci", prompt=message_text, max_tokens=1024, n=1, stop=None, temperature=0.7, )
            bot_response = response.choices[0].text.strip()

            # Send the response back to the user
            say(bot_response)

# Start the app
if __name__ == "__main__":
    app.start(port=int(os.environ["CONTAINER_PORT"]))