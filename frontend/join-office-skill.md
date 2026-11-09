# Join Charisna Office - Agent Skill

## Description
Connect an external or autonomous subagent to the Charisna Visual Agent Desk, enabling real-time status visualization, avatars, and dialogue inside the office.

## Prerequisites
- A valid join key (format: `ocj_xxx`) generated from Charisna Office
- Access to the office endpoint (e.g. `http://localhost:19000`)

## Quick Start

### 1. Register Agent
```bash
python office-agent-push.py --url http://localhost:19000 --name "MyAgent" --key "ocj_xxx"
```

### 2. Push Periodic Status
The script periodically sends heartbeat status (`idle`, `writing`, `syncing`, `error`) with a brief detail summary.
