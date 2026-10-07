# PL FootSmart

A Slack bot that teaches IT concepts through Premier League football analogies. Run `/plfact` in a channel and the bot posts a football fact paired with an IT concept it resembles.

> Example: *"VAR reviews a decision before it's final -> Terraform's plan step reviews changes before apply"*

## Why I built this

I'm learning cloud, security, and software fundamentals, and I find concepts stick better when they're tied to something I already enjoy. This bot is a fun way to practice that, and a project for learning how Slack apps, Socket Mode, and secrets management work.

## How it works

- Built with Python and [Slack Bolt](https://slack.dev/bolt-python/).
- Connects to Slack using **Socket Mode**: the bot opens an outbound connection to Slack, so no public URL or open inbound port is needed.
- A slash command handler (`/plfact`) picks a random entry from a list of football/IT pairs and posts it publicly to the channel using `say()`.
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
4. Under **Slash Commands**, create `/plfact`. The Request URL field is required by the form but isn't used in Socket Mode, so a placeholder works.
5. **Install the app** to your workspace (reinstall after any scope change).

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

You should see `Bolt app is running!`. In Slack, invite the bot to a channel (`/invite @PL FootSmart`) and run `/plfact`.

## Security notes

- `.env`, `.venv`, and `__pycache__` are listed in `.gitignore`, so tokens and generated files are never tracked.
- Never paste tokens into chat, issues, screenshots, or commits. If a token leaks, regenerate it in the Slack app settings.
- The bot uses least-privilege scopes: it can post messages and receive its own slash command, and nothing else.
- Socket Mode means the bot only makes outbound connections, so there's no public endpoint to attack.
- Run it only in a workspace you control.

## Project structure

```
pl-it-bot/
├── bot.py             # Slack app, slash command handler, facts list
├── requirements.txt   # Pinned dependencies
├── .gitignore         # Excludes .env, .venv, __pycache__
└── README.md
```

## Roadmap

Planned, not built yet:

- [ ] Stop the same fact repeating back-to-back (shuffle-and-deal instead of pure random)
- [ ] Grow and fact-check the facts list, with a more conversational tone
- [ ] Scheduled daily fact posts
- [ ] `/plquiz` command for interactive trivia
- [ ] Optional AI-generated analogies (v2)
- [ ] Host it so it runs when my laptop is off (e.g. AWS Lambda with the Events API)

## What I learned

- How Slack apps authenticate: bot tokens vs. app-level tokens, and what each scope grants.
- Why Socket Mode suits a locally-run bot.
- Keeping secrets out of source control with `.env` and `.gitignore`.
- The difference between ephemeral (`respond()`) and public (`say()`) Slack replies.
- Why `random.choice` can repeat results, and how to design around it.
