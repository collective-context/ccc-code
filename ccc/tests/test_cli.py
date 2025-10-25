"""
Tests for CCC CLI commands
"""

import subprocess
import pytest


class TestCLICommands:
    """Test CLI command execution"""
    
    def test_version(self):
        """Test ccc --version"""
        result = subprocess.run(
            ['ccc', '--version'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert 'CCC Production' in result.stdout
    
    def test_help(self):
        """Test ccc --help"""
        result = subprocess.run(
            ['ccc', '--help'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert 'Collective Context Commander' in result.stdout or 'Commander' in result.stdout
    
    def test_info_command(self):
        """Test ccc info"""
        result = subprocess.run(
            ['ccc', 'info'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"info failed: {result.stderr}"
        assert 'CCC Production' in result.stdout
    
    def test_status_command(self):
        """Test ccc status"""
        result = subprocess.run(
            ['ccc', 'status'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert 'Operational' in result.stdout
