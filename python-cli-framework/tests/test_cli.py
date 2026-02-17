"""
Tests for CLI entry point
Built by Jackson Studio
"""

import pytest
from cli.cli import main
import sys


def test_version_flag(capsys, monkeypatch):
    """Test --version flag"""
    monkeypatch.setattr(sys, "argv", ["cli", "--version"])
    
    with pytest.raises(SystemExit) as exc:
        main()
    
    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert "Jackson Studio" in captured.out


def test_help_flag(capsys, monkeypatch):
    """Test --help flag"""
    monkeypatch.setattr(sys, "argv", ["cli", "--help"])
    
    with pytest.raises(SystemExit) as exc:
        main()
    
    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert "Examples:" in captured.out
