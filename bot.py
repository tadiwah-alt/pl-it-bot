import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


load_dotenv()
bot_token = os.environ["SLACK_BOT_TOKEN"]
app_token = os.environ["SLACK_APP_TOKEN"]

if bot_token and app_token:
    print("Bot Token and App Token Loaded")
else:
    print("Failed")


app = App(token=bot_token)

@app.command("/plfact")
def handle_plfact(ack, say):
    ack()
    say("This is a test fact!")


if __name__ == "__main__":
    SocketModeHandler(app, app_token).start()