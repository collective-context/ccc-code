"""Test CCB CLI commands"""
import subprocess
import pytest


class TestCCBCommands:
    """Test CCB command execution"""
    
    def test_version_long(self):
        """Test ccb --version"""
        result = subprocess.run(
            ['ccb', '--version'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"--version failed: {result.stderr}"
        assert 'CCC Beta (ccb)' in result.stdout
    
    def test_version_short(self):
        """Test ccb -v"""
        result = subprocess.run(
            ['ccb', '-v'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"-v failed: {result.stderr}"
        assert 'CCC Beta (ccb)' in result.stdout
    
    def test_help(self):
        """Test ccb --help"""
        result = subprocess.run(
            ['ccb', '--help'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"--help failed: {result.stderr}"
        assert 'CCC Beta' in result.stdout
    
    def test_info_command(self):
        """Test ccb info"""
        result = subprocess.run(
            ['ccb', 'info'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"info failed: {result.stderr}"
        assert 'CCC Beta (ccb)' in result.stdout
        assert 'Available commands' in result.stdout


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
