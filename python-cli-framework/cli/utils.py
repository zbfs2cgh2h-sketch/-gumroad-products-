"""
Common utilities (progress bars, error handling, etc.)
Built by Jackson Studio
"""

import sys
import signal
from typing import Iterable, Callable
from contextlib import contextmanager


class UserError(Exception):
    """User-facing error (clean message, no traceback)"""
    pass


def safe_execute(func: Callable):
    """
    Decorator for clean error handling
    
    UserError → print message, exit 1
    Other exceptions → full traceback, exit 2
    """
    
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UserError as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n\n⏸️  Interrupted by user", file=sys.stderr)
            sys.exit(130)
        except Exception as e:
            print(f"💥 Unexpected error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            sys.exit(2)
    
    return wrapper


def progress_bar(items: Iterable, desc: str = "Processing", total: int = None):
    """
    Simple progress bar (no external deps)
    
    Usage:
        for item in progress_bar(items, desc="Processing files"):
            process(item)
    """
    
    items_list = list(items)
    total = total or len(items_list)
    
    for i, item in enumerate(items_list, 1):
        percent = int(100 * i / total)
        bar = "█" * (percent // 2) + "░" * (50 - percent // 2)
        print(f"\r{desc}: [{bar}] {percent}%", end="", file=sys.stderr)
        yield item
    
    print(file=sys.stderr)  # Newline


@contextmanager
def spinner(message: str = "Loading"):
    """
    Simple spinner for indefinite tasks
    
    Usage:
        with spinner("Downloading data..."):
            download_large_file()
    """
    
    import itertools
    import threading
    import time
    
    done = False
    
    def spin():
        for char in itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"):
            if done:
                break
            print(f"\r{char} {message}", end="", file=sys.stderr)
            time.sleep(0.1)
        print(f"\r✓ {message}", file=sys.stderr)
    
    t = threading.Thread(target=spin)
    t.start()
    
    try:
        yield
    finally:
        done = True
        t.join()


def shutdown_handler(signum, frame):
    """Graceful shutdown on SIGINT/SIGTERM"""
    print("\n\n🛑 Shutting down gracefully...", file=sys.stderr)
    # Cleanup logic here
    sys.exit(0)


# Register signal handlers
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)
