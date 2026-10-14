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
    {
        "football": "VAR reviews a decision before it becomes final.",
        "it": "Terraform's plan command reviews proposed infrastructure changes before they are applied."
    },
    {
        "football": "A red card removes a player from the match immediately.",
        "it": "Revoking an IAM access key immediately cuts off that key's access to cloud resources."
    },
    {
        "football": "Southampton's Shane Long scored the fastest goal in Premier League history after just 7.69 seconds against Watford on 23 April 2019.",
        "it": "A cache can return data in milliseconds, avoiding a slower trip to a database or external API."
    },
    {
        "football": "A football team follows a planned formation, with each player assigned a position and responsibility.",
        "it": "Software follows a defined architecture, with each component assigned a specific responsibility."
    },
    {
        "football": "A pass moves the ball from one player to another.",
        "it": "A network protocol moves data packets from one computer to another."
    },
    {
        "football": "Midfielders control the flow of play, receiving the ball from defenders and supplying attackers.",
        "it": "An API gateway receives client requests, routes them to the correct backend service, and can enforce authentication and rate limits."
    },
    {
        "football": "The referee adds stoppage time at the end of each half to account for delays such as injuries and substitutions.",
        "it": "A timeout or SLA time budget limits how long a request can wait before the system treats it as failed."
    },
    {
        "football": "Defenders protect their own goal and stop opposing attackers from scoring.",
        "it": "Authentication, authorization, and intrusion detection protect a system from unauthorized access, forming defence in depth."
    },
    {
        "football": "A football pitch has boundary lines that define where the ball and players must remain.",
        "it": "Firewalls and security groups define network boundaries and control which traffic can enter or leave a system."
    },
    {
        "football": "A goalkeeper is the only player allowed to handle the ball, and only inside their own penalty area.",
        "it": "Privileged access management gives administrators elevated permissions, but only within a limited scope or environment."
    }
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
    say(f'{chosen["football"]}\n{chosen["it"]}') 


if __name__ == "__main__":
    SocketModeHandler(app, app_token).start()