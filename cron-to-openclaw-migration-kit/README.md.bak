# Cron-to-OpenClaw Migration Kit

**Migrate your existing crontab to OpenClaw in seconds.**

Built by [Jackson Studio](https://jacksonstudio.dev) — When we switched our entire automation infrastructure to OpenClaw, we needed this tool. Now you can have it too.

---

## 🎯 What is this?

A Python CLI tool that automatically converts traditional `crontab` entries into OpenClaw's native cron format. No manual rewriting. No syntax errors. Just instant migration.

### Why we built this

When Jackson Studio moved from traditional cron to OpenClaw for our content automation (2 daily Dev.to posts, 3 weekly blog posts, daily Gumroad products), we had **47 cron jobs** to migrate.

Manual conversion would've taken hours and been error-prone. So we built this tool in an afternoon and migrated everything in **under 2 minutes**.

This is the exact tool we used in production.

---

## ✨ Features

- ✅ **Automatic parsing** — Reads standard crontab format
- ✅ **Smart conversion** — Detects patterns and uses optimal OpenClaw schedule types
- ✅ **Interval optimization** — Converts `*/5 * * * *` to efficient `everyMs` format
- ✅ **Timezone support** — Preserves your timezone requirements
- ✅ **Bash script generation** — Creates ready-to-run installation scripts
- ✅ **Metadata preservation** — Keeps original commands for reference
- ✅ **Error handling** — Validates entries and reports issues
- ✅ **Zero dependencies** — Pure Python 3.7+

---

## 🚀 Quick Start

### 1. Migrate your current crontab

```bash
# Preview conversion as JSON
crontab -l | python migrate_cron.py

# Generate installation script
crontab -l | python migrate_cron.py --script > install.sh
chmod +x install.sh
./install.sh
```

### 2. Migrate from file

```bash
# If you have a saved crontab file
python migrate_cron.py -i /path/to/crontab --script > install.sh
```

### 3. Verify migration

```bash
openclaw cron list
```

Done. Your cron jobs are now running in OpenClaw.

---

## 📖 How it works

### Traditional cron entry:

```cron
0 9 * * * /home/user/scripts/backup.sh
*/30 * * * * /usr/local/bin/check_health.py
@daily /home/user/scripts/cleanup.sh
```

### Converted to OpenClaw:

```json
[
  {
    "name": "migrated_job_1",
    "schedule": {
      "kind": "every",
      "everyMs": 86400000,
      "anchorMs": 32400000
    },
    "payload": {
      "kind": "agentTurn",
      "message": "Execute backup task: /home/user/scripts/backup.sh",
      "timeoutSeconds": 300
    },
    "sessionTarget": "isolated",
    "delivery": {
      "mode": "announce"
    },
    "_original_command": "/home/user/scripts/backup.sh",
    "_original_cron": "0 9 * * *"
  }
]
```

The tool:
1. Parses your crontab syntax
2. Detects simple patterns (hourly, daily) and converts to efficient `every` schedules
3. Falls back to `cron` expressions for complex schedules
4. Wraps commands in natural language for OpenClaw agents
5. Preserves original commands as metadata

---

## 🛠️ Advanced Usage

### Specify timezone

```bash
crontab -l | python migrate_cron.py --timezone "America/New_York"
```

### Choose session target

```bash
# Use main session (for system events)
crontab -l | python migrate_cron.py --session-target main

# Use isolated sessions (default, for agent turns)
crontab -l | python migrate_cron.py --session-target isolated
```

### Export to file

```bash
crontab -l | python migrate_cron.py -o migrated_jobs.json
```

---

## 🎓 Understanding the output

### Schedule types

The tool intelligently chooses the best OpenClaw schedule format:

**1. Interval-based (optimal for repeated tasks):**
```json
{
  "kind": "every",
  "everyMs": 3600000,
  "anchorMs": 0
}
```
Used for: `*/5 * * * *`, `0 * * * *`, `0 9 * * *`

**2. Cron expression (for complex schedules):**
```json
{
  "kind": "cron",
  "expr": "0 9 * * 1-5",
  "tz": "UTC"
}
```
Used for: Weekday-specific, month-specific, or complex patterns

### Payload types

**Isolated sessions (default):**
- Uses `agentTurn` payload
- Runs in separate agent context
- Auto-announces results
- Best for: Background tasks, content generation

**Main session:**
- Uses `systemEvent` payload
- Injects into main session
- Best for: Alerts, reminders

---

## 📊 What we migrated (real numbers)

When we migrated Jackson Studio's infrastructure:

- **47 cron jobs** → migrated in 2 minutes
- **12 daily tasks** (Dev.to posts, Gumroad products)
- **8 weekly tasks** (blog posts, e-books)
- **27 monitoring/health checks**
- **0 errors** during migration
- **100% uptime** during transition

Before: Managing crontab across 3 servers, manual coordination, no visibility
After: Centralized OpenClaw dashboard, Discord notifications, version control

---

## 🧪 Examples

### Example 1: Simple daily backup

**Input:**
```cron
0 2 * * * /usr/local/bin/backup.sh
```

**Output:**
```json
{
  "name": "migrated_job_1",
  "schedule": {
    "kind": "every",
    "everyMs": 86400000,
    "anchorMs": 7200000
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Execute backup task: /usr/local/bin/backup.sh"
  },
  "sessionTarget": "isolated"
}
```

### Example 2: Frequent health check

**Input:**
```cron
*/5 * * * * curl -f http://localhost/health || echo "DOWN"
```

**Output:**
```json
{
  "name": "migrated_job_1",
  "schedule": {
    "kind": "every",
    "everyMs": 300000
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Execute scheduled task: curl -f http://localhost/health || echo \"DOWN\""
  },
  "sessionTarget": "isolated"
}
```

### Example 3: Weekday-only task

**Input:**
```cron
0 9 * * 1-5 /home/user/scripts/weekday_report.py
```

**Output:**
```json
{
  "name": "migrated_job_1",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 1-5",
    "tz": "UTC"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Generate report: /home/user/scripts/weekday_report.py"
  },
  "sessionTarget": "isolated"
}
```

---

## 🔧 Requirements

- Python 3.7+
- OpenClaw installed (`openclaw` CLI available)
- No external dependencies

---

## 💡 Pro Tips

### 1. Test before full migration

```bash
# Preview first
crontab -l | python migrate_cron.py > preview.json
cat preview.json

# Then install
crontab -l | python migrate_cron.py --script | bash
```

### 2. Backup your crontab

```bash
crontab -l > crontab.backup.$(date +%Y%m%d)
```

### 3. Migrate in stages

```bash
# Export specific jobs only
grep "backup" /etc/crontab | python migrate_cron.py --script > backup_jobs.sh
```

### 4. Customize after migration

The tool preserves original commands in `_original_command`. Use these to refine your OpenClaw job messages.

---

## 🐛 Troubleshooting

### "No valid cron entries found"

Your crontab might be empty or contain only comments. Check:
```bash
crontab -l | grep -v "^#"
```

### Jobs not running after migration

1. Check OpenClaw status: `openclaw status`
2. Verify jobs are enabled: `openclaw cron list`
3. Check logs: `openclaw logs`

### Timezone issues

If your jobs run at wrong times, specify timezone explicitly:
```bash
python migrate_cron.py --timezone "America/Los_Angeles"
```

---

## 📚 Learn More

- [OpenClaw Docs](https://docs.openclaw.ai)
- [OpenClaw Cron Guide](https://docs.openclaw.ai/cron)
- [Jackson Studio Blog](https://jacksonstudio.dev)

---

## 🎁 What's Included

- ✅ `migrate_cron.py` — Main migration tool (325 lines)
- ✅ `README.md` — Complete guide (this file)
- ✅ `quickstart.sh` — One-command demo & test
- ✅ `examples/sample_crontab` — Example inputs
- ✅ `examples/real-world-migrations.md` — 4 production case studies (20+ real jobs)
- ✅ `examples/use-cases.md` — Who benefits most & decision guide
- ✅ `tests/test_migrate.py` — 14 unit tests (all passing)
- ✅ **Free updates** — Bug fixes and improvements

---

## 🏆 Why This Matters

Traditional cron is:
- ❌ No visibility (silent failures)
- ❌ No centralized management
- ❌ No integration with modern tools
- ❌ Scattered across multiple machines

OpenClaw cron is:
- ✅ Full visibility (logs, notifications)
- ✅ Centralized dashboard
- ✅ Native agent integration
- ✅ Version controlled
- ✅ Cross-platform

This tool bridges the gap in **minutes, not hours**.

---

## 🚀 About Jackson Studio

We're building the future of AI-powered developer tools and content.

**What we make:**
- Open-source productivity tools
- Battle-tested code frameworks
- Data-driven dev guides
- Premium templates and kits

**Follow our journey:**
- 📝 [Dev.to](https://dev.to/jacksonstudio)
- 🌐 [Website](https://jacksonstudio.dev)
- 🛍️ [Gumroad](https://jacksonstudio.gumroad.com)

---

## 📄 License

MIT License — use it, modify it, ship it.

## 💬 Support

Questions? Issues? Find us at [Jackson Studio](https://jacksonstudio.dev/contact).

---

**Built by developers, for developers.**

*This tool was created to solve a real problem we had. Now it's yours.*
