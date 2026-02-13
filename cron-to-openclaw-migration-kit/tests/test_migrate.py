#!/usr/bin/env python3
"""
Unit tests for Cron-to-OpenClaw Migration Kit
"""

import unittest
from migrate_cron import CronParser, OpenClawCronGenerator, CronMigrator


class TestCronParser(unittest.TestCase):
    
    def test_parse_standard_cron(self):
        result = CronParser.parse_crontab_line("0 9 * * * /usr/bin/backup.sh")
        self.assertEqual(result[0], 'cron')
        self.assertEqual(result[1], '0 9 * * *')
        self.assertEqual(result[2], '/usr/bin/backup.sh')
    
    def test_parse_special_schedule(self):
        result = CronParser.parse_crontab_line("@daily /usr/bin/cleanup.sh")
        self.assertEqual(result[0], 'cron')
        self.assertEqual(result[1], '0 0 * * *')
        self.assertEqual(result[2], '/usr/bin/cleanup.sh')
    
    def test_parse_comment(self):
        result = CronParser.parse_crontab_line("# This is a comment")
        self.assertEqual(result[0], 'comment')
    
    def test_parse_empty_line(self):
        result = CronParser.parse_crontab_line("")
        self.assertIsNone(result)
    
    def test_cron_to_interval_hourly(self):
        result = CronParser.cron_to_interval("0 * * * *")
        self.assertEqual(result['kind'], 'every')
        self.assertEqual(result['everyMs'], 3600000)
    
    def test_cron_to_interval_daily(self):
        result = CronParser.cron_to_interval("0 9 * * *")
        self.assertEqual(result['kind'], 'every')
        self.assertEqual(result['everyMs'], 86400000)
        self.assertEqual(result['anchorMs'], 32400000)  # 9 hours in ms
    
    def test_cron_to_interval_complex(self):
        # Should return None for complex patterns
        result = CronParser.cron_to_interval("0 9 * * 1-5")
        self.assertIsNone(result)


class TestOpenClawCronGenerator(unittest.TestCase):
    
    def test_generate_isolated_job(self):
        schedule = {'kind': 'every', 'everyMs': 3600000}
        job = OpenClawCronGenerator.generate_job(
            name="test_job",
            schedule=schedule,
            command="Test command",
            session_target="isolated"
        )
        
        self.assertEqual(job['name'], 'test_job')
        self.assertEqual(job['sessionTarget'], 'isolated')
        self.assertEqual(job['payload']['kind'], 'agentTurn')
        self.assertIn('delivery', job)
    
    def test_generate_main_job(self):
        schedule = {'kind': 'every', 'everyMs': 3600000}
        job = OpenClawCronGenerator.generate_job(
            name="test_job",
            schedule=schedule,
            command="Test command",
            session_target="main"
        )
        
        self.assertEqual(job['sessionTarget'], 'main')
        self.assertEqual(job['payload']['kind'], 'systemEvent')
        self.assertNotIn('delivery', job)
    
    def test_command_to_message_backup(self):
        message = OpenClawCronGenerator.command_to_message("/usr/bin/backup.sh")
        self.assertIn("backup", message.lower())
    
    def test_command_to_message_script(self):
        message = OpenClawCronGenerator.command_to_message("/home/user/daily_report.py")
        self.assertIn("daily report", message.lower())


class TestCronMigrator(unittest.TestCase):
    
    def test_migrate_simple_crontab(self):
        crontab_lines = [
            "0 9 * * * /usr/bin/backup.sh",
            "*/30 * * * * /usr/bin/health_check.py"
        ]
        
        migrator = CronMigrator()
        jobs = migrator.migrate_crontab(crontab_lines)
        
        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0]['sessionTarget'], 'isolated')
        self.assertIn('_original_command', jobs[0])
    
    def test_migrate_with_comments(self):
        crontab_lines = [
            "# Daily backup",
            "0 9 * * * /usr/bin/backup.sh",
            "",
            "# Health check",
            "*/30 * * * * /usr/bin/health_check.py"
        ]
        
        migrator = CronMigrator()
        jobs = migrator.migrate_crontab(crontab_lines)
        
        # Should skip comments and empty lines
        self.assertEqual(len(jobs), 2)
    
    def test_generate_migration_script(self):
        jobs = [
            {
                "name": "test_job",
                "schedule": {"kind": "every", "everyMs": 3600000},
                "payload": {"kind": "agentTurn", "message": "Test"},
                "sessionTarget": "isolated"
            }
        ]
        
        migrator = CronMigrator()
        script = migrator.generate_migration_script(jobs)
        
        self.assertIn("#!/bin/bash", script)
        self.assertIn("openclaw cron add", script)
        self.assertIn("test_job", script)


if __name__ == '__main__':
    unittest.main()
