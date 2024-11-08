from slack_bolt import App
from dotenv import load_dotenv
import os

load_dotenv()
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.event("message")
def handle_dm_messages(event, say):
    # only echo if it's a direct message
    if event.get("channel_type") == "im":
        user_message = event.get("text")
        say(text=user_message)
        say(text="test auto deploy again!")

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
