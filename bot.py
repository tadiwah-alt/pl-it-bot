import os
import random
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

## Establish connection to the Slack app
load_dotenv()
bot_token = os.environ["SLACK_BOT_TOKEN"]
app_token = os.environ["SLACK_APP_TOKEN"]


## Dictionary containing facts
facts = [
    {"football": "VAR reviews a decision before it's final", "it": "Terraform's plan step reviews changes before apply"},
    {"football": "A red card removes a player instantly", "it": "Revoking an IAM key instantly cuts off access"},
    {"football": "Southampton player Shane Long scored against Watford just 7.69 seconds after kickoff on 23 April 2019, the fastest goal in Premier League history", "it": "Think of kickoff as a request arriving and the goal as the response. The time between them is your football version of response latency"},
    {"football": "Players follow a planned formation", "it": "Software components follow a defined architecture"},
    {"football": "A pass moves the ball from one player to another", "it": "A network sends data from one computer to another"}
]


## Copy the facts dictionary into deck
deck = facts.copy()



## Confirm connection to Slack has been established or failed
if bot_token and app_token:
    print("Bot Token and App Token Loaded")
else:
    print("Failed")




app = App(token=bot_token)


## plfact command handler
@app.command("/plfact")
def handle_plfact(ack, say):
    ack()
    global deck

    if not deck:
        deck = facts.copy() 
    
    
    

    ## Shuffle deck then pick a random fact from deck and post it
    random.shuffle(deck)
    chosen = deck.pop()
    say(f'{chosen["football"]} -> {chosen["it"]}') 


if __name__ == "__main__":
    SocketModeHandler(app, app_token).start()