---
name: hermes-bot-manager
description: Use when managing Hermes bots, routines, and groups.
version: 1.0.0
author: PatchworkMD
license: MIT
tags:
  - hermes
  - bots
  - automation
  - desktop
related_skills:
  - austin-smart-model-router
  - active-skill-update
---

# Hermes Bot Manager

Use this when the work is creating, editing, or operating Hermes bots and their routines, chat, or groups. A bot is just a Hermes profile; Bot Mode is the desktop UI over it.

## When to Use

- Create, edit, or manage Hermes bot profiles
- Set up bot routines, groups, or multi-machine roster entries
- Translate Bot Mode UI actions into CLI equivalents
- Verify bot configuration after changes

## Setup

1. Create the profile.
2. Set identity fields.
3. Attach skills, toolsets, MCPs, and model pin.
4. Add routines as cron jobs.
5. Verify with CLI parity checks.

### Create

```bash
hermes profile create <name>
hermes profile list
```

### Edit

```bash
hermes -p <name> chat --in ~ -c "Bot Chat" --create-if-missing -Q -q "Edit profile"
```

Or edit directly:
- `~/.hermes/profiles/<name>/config.yaml`
- `~/.hermes/profiles/<name>/SOUL.md`
- `~/.hermes/profiles/<name>/skills/`

### Identity

Set avatar, title, and description in the profile metadata. The desktop roster shows avatar, latest preview, and timestamp. Right-click a Bot to duplicate or delete it.

## Routines

Use the cron system with the namespace `[bot:<name>] <routine>`.

```bash
hermes cron list | grep '\[bot:<name>\]'
```

Runs land in the Bot's canonical chat. For advanced behavior, use:
- `monitor_script` or `monitor_url` for change detection
- `continuity` for incremental work across runs
- `deliver` for routing output

## Groups

Right-click a Bot → Move to group. Group chats are 2–6 bots. Open chat on the group header to create a shared room. Ungrouped bots stay on top; groups are alphabetical; empty groups disappear.

## Bot-to-bot messaging

Use `@name` in any Bot Chat. The canonical Bot Chat receives the bot protocol when `agent.bot_mode_protocol` is true in `config.yaml`. Delivery is per-invocation; the receiving bot picks it up on next run.

## Multi-machine

Register multiple connections in Settings → Connections. New Agent dialog shows Create on when more than one connection exists. Remote bots show as `@name-device`. Clicking a Connections Bot does not switch your window; message or group chat instead.

## Turn off

Bot Mode is a desktop plugin. Disable in Settings → Plugins → Bots. Profiles, sessions, and cron jobs remain intact.

## Verification

Before claiming completion, verify:
- `hermes profile list` shows the bot
- `hermes -p <bot> chat` opens the expected agent
- `hermes cron list` shows routine jobs named `[bot:<bot>] ...`
- Bot Chat delivers routine results

## Common mistakes

- Editing the wrong profile directory. Always confirm the profile name before editing files.
- Forgetting the `[bot:<name>]` namespace. Cron jobs without it still run, but Bot Mode may not associate them with the bot.
- Assuming bot chats behave like regular sessions. Bot Chats keep history across `/compact`; regular sessions allow `/new`.
- Expecting live interrupt. Bot-to-bot delivery happens on next run, not mid-conversation.
