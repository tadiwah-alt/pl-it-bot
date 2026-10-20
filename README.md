# PL FootSmart

A Slack bot that teaches IT concepts through Premier League football analogies. Run `/plfact` in a channel and the bot posts a football fact paired with an IT concept it resembles. Run `/plquiz` to test yourself.

> Example: *"VAR reviews a decision before it's final -> Terraform's plan step reviews changes before apply"*

## Why I built this

I'm learning cloud, security, and software fundamentals, and I find concepts stick better when they're tied to something I already enjoy. This bot is a fun way to practice that, and a project for learning how Slack apps, Socket Mode, and secrets management work.

## Commands

| Command | What it does |
|---|---|
| `/plfact` | Posts a football fact and the IT concept it resembles. Facts are dealt from a shuffled deck, so none repeats until every fact has been shown. |
| `/plquiz` | Posts a multiple-choice question that links a football idea to an IT concept. |
| `/plreveal` | Reveals the answer and explanation for the current quiz question. |
| `/plreveal 2` | Submits your answer (the choice number). You get private feedback saying whether it was correct, plus the explanation. |

Invalid guesses (not a number, or outside the range of choices) are rejected with a hint, and the question stays active so you can try again.

## How it works

- Built with Python and [Slack Bolt](https://slack.dev/bolt-python/).
- Connects to Slack using **Socket Mode**: the bot opens an outbound connection to Slack, so no public URL or open inbound port is needed.
- `/plfact` shuffles a copy of the facts list and deals one fact at a time, refilling the deck when it runs out.
- `/plquiz` picks a random question from the quiz list and stores it as the current question.
- `/plreveal` reads the stored question. With no argument it reveals the answer publicly. With a number it checks the guess and replies privately using `respond()`.
- Secrets are loaded from a `.env` file using `python-dotenv` and are never committed to the repo.

## Tech stack

| Piece | Purpose |
|---|---|
| Python 3 | Bot logic |
| `slack_bolt` | Slack app framework (commands, Socket Mode) |
| `python-dotenv` | Loads tokens from `.env` |

## Setup

### 1. Create the Slack app

1. Go to [api.slack.com/apps](https://api.slack.com/apps) and create an app **from scratch** in a workspace you own or administer.
2. Under **OAuth & Permissions**, add these **Bot Token Scopes** (and nothing broader):
   - `chat:write`
   - `commands`
3. Under **Socket Mode**, enable it and generate an **App-Level Token** with the `connections:write` scope.
4. Under **Slash Commands**, create `/plfact`, `/plquiz`, and `/plreveal`. For `/plreveal`, add a usage hint such as `[choice number]`. The Request URL field is required by the form but isn't used in Socket Mode, so a placeholder works.
5. **Install the app** to your workspace (reinstall after any scope or command change if Slack asks).

### 2. Run locally

```bash
git clone git@github.com:tadiwah-alt/pl-it-bot.git
cd pl-it-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-level-token
```

Start the bot:

```bash
python bot.py
```

You should see `Bolt app is running!`. In Slack, invite the bot to a channel (`/invite @PL FootSmart`) and run `/plfact` or `/plquiz`.

## Security notes

- `.env`, `.venv`, and `__pycache__` are listed in `.gitignore`, so tokens and generated files are never tracked.
- Never paste tokens into chat, issues, screenshots, or commits. If a token leaks, regenerate it in the Slack app settings.
- The bot uses least-privilege scopes: it can post messages and receive its own slash commands, and nothing else.
- Socket Mode means the bot only makes outbound connections, so there's no public endpoint to attack.
- User input to `/plreveal` is validated before use: non-numeric and out-of-range values are rejected without crashing the bot or ending the quiz round.
- Run it only in a workspace you control.

## Project structure

```
pl-it-bot/
├── bot.py             # Slack app, slash command handlers, facts and quiz data
├── requirements.txt   # Pinned dependencies
├── .gitignore         # Excludes .env, .venv, __pycache__
└── README.md
```

## Known limitations

- The bot stores **one** active quiz question for the whole workspace. If two people run `/plquiz` in different channels, the second question replaces the first.
- State lives in memory, so it resets whenever the bot restarts.
- The bot only runs while my laptop is on.

## Roadmap

Done:

- [x] Stop the same fact repeating back-to-back (shuffle-and-deal instead of pure random)
- [x] Grow and fact-check the facts list, with a more conversational tone
- [x] `/plquiz` command for interactive trivia
- [x] `/plreveal` command to display the answer with an explanation
- [x] `/plreveal [number]` to submit an answer and get private feedback

Planned:

- [ ] Scheduled daily fact posts
- [ ] Track quiz state per channel or per user instead of one global question
- [ ] Optional AI-generated analogies (v2)
- [ ] Host it so it runs when my laptop is off (free tier only)

## What I learned

- How Slack apps authenticate: bot tokens vs. app-level tokens, and what each scope grants.
- Why Socket Mode suits a locally-run bot.
- Keeping secrets out of source control with `.env` and `.gitignore`.
- The difference between ephemeral (`respond()`) and public (`say()`) Slack replies.
- Why `random.choice` can repeat results, and how to design around it with a shuffled deck.
- Why a function needs `global` to reassign a module-level variable, while in-place changes like `pop()` and `shuffle()` don't.
- Why user input must be validated before use: Slack sends an empty string, not `None`, when no argument is typed, and `int()` raises an error on non-numbers.