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
        "Football": "VAR reviews a decision before it becomes final.",
        "IT": "Terraform's plan command reviews proposed infrastructure changes before they are applied."
    },
    {
        "Football": "A red card removes a player from the match immediately.",
        "IT": "Revoking an IAM access key immediately cuts off that key's access to cloud resources."
    },
    {
        "Football": "Southampton's Shane Long scored the fastest goal in Premier League history after just 7.69 seconds against Watford in April 2019.",
        "IT": "A cache can return data in milliseconds, avoiding a slower trip to a database or external API."
    },
    {
        "Football": "A football team follows a planned formation, with each player assigned a position and responsibility.",
        "IT": "Software follows a defined architecture, with each component assigned a specific responsibility."
    },
    {
        "Football": "A pass moves the ball from one player to another.",
        "IT": "A network protocol moves data packets from one computer to another."
    },
    {
        "Football": "Midfielders control the flow of play, receiving the ball from defenders and supplying attackers.",
        "IT": "An API gateway receives client requests, routes them to the correct backend service, and can enforce authentication and rate limits."
    },
    {
        "Football": "The referee adds stoppage time at the end of each half to account for delays such as injuries and substitutions.",
        "IT": "A timeout or SLA time budget limits how long a request can wait before the system treats it as failed."
    },
    {
        "Football": "Defenders protect their own goal and stop opposing attackers from scoring.",
        "IT": "Authentication, authorization, and intrusion detection protect a system from unauthorized access, forming defence in depth."
    },
    {
        "Football": "A football pitch has boundary lines that define where the ball and players must remain.",
        "IT": "Firewalls and security groups define network boundaries and control which traffic can enter or leave a system."
    },
    {
        "Football": "A goalkeeper is the only player allowed to handle the ball, and only inside their own penalty area during open play.",
        "IT": "Privileged access management gives administrators elevated permissions, but only within a limited scope or environment."
    }
]




## Dictionary containing quiz and answers
quiz = [
    {
        "question": "In football, VAR reviews a decision before it becomes final. Which IT concept matches this behaviour?",
        "choices": [
            "Continuous Integration (CI) pipeline",
            "Terraform plan command",
            "Load balancer health checks"
        ],
        "answer": 2,
        "explanation": "Terraform's plan command previews changes before they are applied, just like VAR reviews a decision before it becomes final."
    },
    
    {
        "question": "A red card removes a player from the match immediately. Which IT concept behaves similarly?",
        "choices": [
            "Revoking an IAM access key",
            "Rotating logs",
            "Horizontal autoscaling"
        ],
        "answer": 1,
        "explanation": "Revoking an IAM access key instantly cuts off access, just like a red card immediately removes a player from the game."
    },

    {
        "question": "Midfielders control the flow of play, receiving the ball from defenders and supplying attackers. Which IT concept matches this role?",
        "choices": [
            "API gateway",
            "DNS resolver",
            "Message queue"
        ],
        "answer": 1,
        "explanation": "An API gateway receives requests, routes them to the correct backend, and manages flow—similar to midfielders controlling play."
    },

    {
        "question": "A football pitch has boundary lines that define where the ball and players must remain. Which IT concept reflects this idea?",
        "choices": [
            "Distributed tracing spans",
            "Load balancer routing rules",
            "Firewalls and security groups"
            
        ],
        "answer": 3,
        "explanation": "Firewalls and security groups define network boundaries and control what traffic can enter or leave, just like pitch boundary lines."
    },

    {
        "question": "Defenders protect their goal and stop attackers from scoring. Which IT concept plays a similar defensive role?",
        "choices": [
            "Container orchestration",
            "Authentication, authorization, and intrusion detection",
            "Data replication"
        ],
        "answer": 2,
        "explanation": "Authentication, authorization, and intrusion detection form layers of defence that prevent unauthorized access, similar to defenders stopping attacks."
    },

    {
        "question": "A goalkeeper has special privileges: they can handle the ball, but only inside their penalty area. Which IT concept matches this?",
        "choices": [
            "Content delivery networks",
            "Privileged access management",
            "Event-driven architecture"
        ],
        "answer": 2,
        "explanation": "Privileged access management grants elevated permissions but only within a limited scope, just like a goalkeeper's restricted special abilities."
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
question = None


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
    say(f'{chosen["Football"]}\n{chosen["IT"]}') 




## plreveal command handler
@app.command("/plreveal")
def handle_plreveal(ack, say):
    ack()
    global question

    if question is None:
        say("There isn't a quiz question to reveal yet. Run /plquiz first.")
        return

    answer = question["choices"][question["answer"] - 1]
    say(f'Answer: {answer}\n{question["explanation"]}')
    question = None




## plquiz command handler
@app.command("/plquiz")
def handle_plquiz(ack, say):
    ack()

##Randomly chose a question form quiz and display it
    global question
    question = random.choice(quiz)
    choices = question["choices"]
    formatted = "\n".join(
        f'{number}. {choice}'
        for number, choice in enumerate(choices, start=1)
    )
    say(f'{question["question"]}\n{formatted}')







if __name__ == "__main__":
    SocketModeHandler(app, app_token).start()