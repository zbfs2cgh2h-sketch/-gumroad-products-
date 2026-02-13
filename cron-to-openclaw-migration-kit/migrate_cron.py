#!/usr/bin/env python3
"""
Cron-to-OpenClaw Migration Kit
Automatically convert crontab entries to OpenClaw cron format

Built by Jackson Studio
https://jacksonstudio.dev
"""

import argparse
import json
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class CronParser:
    """Parse traditional crontab entries"""
    
    CRON_REGEX = re.compile(
        r'^([@#].*|(\S+\s+\S+\s+\S+\s+\S+\s+\S+)\s+(.+))$'
    )
    
    SPECIAL_SCHEDULES = {
        '@yearly': '0 0 1 1 *',
        '@annually': '0 0 1 1 *',
        '@monthly': '0 0 1 * *',
        '@weekly': '0 0 * * 0',
        '@daily': '0 0 * * *',
        '@midnight': '0 0 * * *',
        '@hourly': '0 * * * *',
    }
    
    @staticmethod
    def parse_crontab_line(line: str) -> Optional[Tuple[str, str, str]]:
        """Parse a single crontab line"""
        line = line.strip()
        
        # Skip empty lines
        if not line:
            return None
        
        # Handle comments
        if line.startswith('#'):
            return ('comment', line, '')
        
        # Handle special schedules
        for special, cron_expr in CronParser.SPECIAL_SCHEDULES.items():
            if line.startswith(special):
                command = line[len(special):].strip()
                return ('cron', cron_expr, command)
        
        # Parse standard cron format
        match = CronParser.CRON_REGEX.match(line)
        if match:
            if match.group(2):  # Standard cron format
                return ('cron', match.group(2), match.group(3))
        
        return None
    
    @staticmethod
    def cron_to_interval(cron_expr: str) -> Optional[Dict]:
        """Convert simple cron expressions to interval-based schedule"""
        parts = cron_expr.split()
        if len(parts) != 5:
            return None
        
        minute, hour, day, month, weekday = parts
        
        # Detect hourly pattern
        if hour == '*' and day == '*' and month == '*' and weekday == '*':
            if minute == '*':
                return {'kind': 'every', 'everyMs': 3600000}  # Every hour
            if minute.isdigit():
                offset_ms = int(minute) * 60 * 1000
                return {'kind': 'every', 'everyMs': 3600000, 'anchorMs': offset_ms}
        
        # Detect daily pattern
        if day == '*' and month == '*' and weekday == '*':
            if hour.isdigit() and minute.isdigit():
                hour_ms = int(hour) * 3600000 + int(minute) * 60000
                return {'kind': 'every', 'everyMs': 86400000, 'anchorMs': hour_ms}
        
        return None


class OpenClawCronGenerator:
    """Generate OpenClaw cron job definitions"""
    
    @staticmethod
    def generate_job(
        name: str,
        schedule: Dict,
        command: str,
        session_target: str = "isolated",
        enabled: bool = True
    ) -> Dict:
        """Generate OpenClaw cron job JSON"""
        
        # Determine payload type based on session target
        if session_target == "main":
            payload = {
                "kind": "systemEvent",
                "text": command
            }
        else:  # isolated
            payload = {
                "kind": "agentTurn",
                "message": command,
                "timeoutSeconds": 300
            }
        
        job = {
            "name": name,
            "schedule": schedule,
            "payload": payload,
            "sessionTarget": session_target,
            "enabled": enabled
        }
        
        # Add delivery for isolated agentTurn
        if session_target == "isolated" and payload["kind"] == "agentTurn":
            job["delivery"] = {
                "mode": "announce"
            }
        
        return job
    
    @staticmethod
    def command_to_message(command: str) -> str:
        """Convert shell command to natural language message"""
        # Extract script name if present
        if command.endswith('.sh') or command.endswith('.py'):
            script_name = command.split('/')[-1].replace('_', ' ').replace('.sh', '').replace('.py', '')
            return f"Run the {script_name} task"
        
        # Handle common patterns
        if 'backup' in command.lower():
            return f"Execute backup task: {command}"
        if 'cleanup' in command.lower():
            return f"Run cleanup task: {command}"
        if 'report' in command.lower():
            return f"Generate report: {command}"
        
        return f"Execute scheduled task: {command}"


class CronMigrator:
    """Main migration orchestrator"""
    
    def __init__(self, timezone: str = "UTC"):
        self.timezone = timezone
        self.parser = CronParser()
        self.generator = OpenClawCronGenerator()
    
    def migrate_crontab(self, crontab_lines: List[str]) -> List[Dict]:
        """Migrate entire crontab to OpenClaw format"""
        jobs = []
        
        for idx, line in enumerate(crontab_lines):
            parsed = self.parser.parse_crontab_line(line)
            
            if not parsed:
                continue
            
            entry_type, schedule_or_comment, command = parsed
            
            if entry_type == 'comment':
                # Skip comments but could be preserved in metadata
                continue
            
            if entry_type == 'cron':
                # Try to convert to interval first
                interval_schedule = self.parser.cron_to_interval(schedule_or_comment)
                
                if interval_schedule:
                    schedule = interval_schedule
                else:
                    # Fall back to cron expression
                    schedule = {
                        'kind': 'cron',
                        'expr': schedule_or_comment,
                        'tz': self.timezone
                    }
                
                # Generate job name
                job_name = f"migrated_job_{idx + 1}"
                
                # Convert command to message
                message = self.generator.command_to_message(command)
                
                # Create job
                job = self.generator.generate_job(
                    name=job_name,
                    schedule=schedule,
                    command=message,
                    session_target="isolated"
                )
                
                # Add original command as metadata
                job['_original_command'] = command
                job['_original_cron'] = schedule_or_comment
                
                jobs.append(job)
        
        return jobs
    
    def generate_migration_script(self, jobs: List[Dict]) -> str:
        """Generate bash script to add jobs to OpenClaw"""
        script_lines = [
            "#!/bin/bash",
            "# OpenClaw Cron Migration Script",
            "# Generated by Cron-to-OpenClaw Migration Kit",
            "# Built by Jackson Studio",
            "",
            "set -e",
            "",
            "echo '🔄 Starting OpenClaw cron migration...'",
            ""
        ]
        
        for idx, job in enumerate(jobs):
            job_json = json.dumps(job, indent=2)
            script_lines.extend([
                f"echo '📝 Adding job {idx + 1}/{len(jobs)}: {job['name']}'",
                f"cat <<'EOF' | openclaw cron add -",
                job_json,
                "EOF",
                ""
            ])
        
        script_lines.extend([
            "echo '✅ Migration complete!'",
            "echo ''",
            "echo 'To verify, run: openclaw cron list'",
            ""
        ])
        
        return '\n'.join(script_lines)


def main():
    parser = argparse.ArgumentParser(
        description='Migrate crontab to OpenClaw cron format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Migrate current user's crontab
  crontab -l | python migrate_cron.py
  
  # Migrate from file
  python migrate_cron.py -i /path/to/crontab
  
  # Generate installation script
  crontab -l | python migrate_cron.py --script > install.sh
  chmod +x install.sh
  ./install.sh
  
Built by Jackson Studio
https://jacksonstudio.dev
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='Input crontab file (default: stdin)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='Output file (default: stdout)'
    )
    
    parser.add_argument(
        '--timezone',
        default='UTC',
        help='Timezone for cron expressions (default: UTC)'
    )
    
    parser.add_argument(
        '--script',
        action='store_true',
        help='Generate bash installation script instead of JSON'
    )
    
    parser.add_argument(
        '--session-target',
        choices=['main', 'isolated'],
        default='isolated',
        help='Target session type (default: isolated)'
    )
    
    args = parser.parse_args()
    
    # Read crontab
    crontab_lines = args.input.readlines()
    
    # Migrate
    migrator = CronMigrator(timezone=args.timezone)
    jobs = migrator.migrate_crontab(crontab_lines)
    
    if not jobs:
        print("⚠️  No valid cron entries found", file=sys.stderr)
        sys.exit(1)
    
    # Output
    if args.script:
        script = migrator.generate_migration_script(jobs)
        args.output.write(script)
    else:
        # Output as JSON array
        json.dump(jobs, args.output, indent=2)
        args.output.write('\n')
    
    # Stats to stderr
    print(f"✅ Converted {len(jobs)} cron jobs", file=sys.stderr)


if __name__ == '__main__':
    main()
