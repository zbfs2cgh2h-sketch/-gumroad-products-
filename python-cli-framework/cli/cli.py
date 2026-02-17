#!/usr/bin/env python3
"""
Main CLI entry point with subcommands
Built by Jackson Studio
"""

import argparse
import sys
from cli.logging import get_logger, setup_logging
from cli.config import load_config
from cli.update import check_for_updates
from cli import __version__

logger = get_logger(__name__)


def cmd_run(args):
    """Example: run command"""
    logger.info("Running command", extra={"input": args.input, "verbose": args.verbose})
    # Your logic here
    print(f"Processing: {args.input}")


def cmd_config(args):
    """Example: config command"""
    config = load_config(args.config)
    logger.info("Config loaded", extra={"config_file": args.config})
    print(config)


def main():
    parser = argparse.ArgumentParser(
        description="Python CLI Framework — Built by Jackson Studio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s run --input data.csv
  %(prog)s config --config custom.yaml
  %(prog)s --version
        """
    )
    
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__} (Built by Jackson Studio)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument("--log-format", choices=["text", "json"], default="text", help="Log output format")
    parser.add_argument("--config", "-c", help="Config file path (default: config.yaml)")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Subcommand: run
    run_parser = subparsers.add_parser("run", help="Run the main task")
    run_parser.add_argument("--input", "-i", required=True, help="Input file or data")
    run_parser.set_defaults(func=cmd_run)
    
    # Subcommand: config
    config_parser = subparsers.add_parser("config", help="Show current config")
    config_parser.set_defaults(func=cmd_config)
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(level=log_level, log_format=args.log_format)
    
    # Check for updates (non-blocking, once per 24h)
    check_for_updates(current_version=__version__, repo="jackson-studio/python-cli-framework")
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute subcommand
    try:
        args.func(args)
    except Exception as e:
        logger.error("Command failed", extra={"error": str(e)}, exc_info=True)
        sys.exit(2)


if __name__ == "__main__":
    main()
