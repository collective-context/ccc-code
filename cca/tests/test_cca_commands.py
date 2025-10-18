"""Test CCA Commands"""
import subprocess
import pytest


class TestCCACommands:
    """Test CCA command execution"""
    
    def test_version_long(self):
        """Test cca --version"""
        result = subprocess.run(['cca', '--version'], capture_output=True, text=True)
        assert result.returncode == 0, f"--version failed: {result.stderr}"
        assert 'CCC Alpha (cca)' in result.stdout, "Version output incorrect"
    
    def test_version_short(self):
        """Test cca -v"""
        result = subprocess.run(['cca', '-v'], capture_output=True, text=True)
        assert result.returncode == 0, f"-v failed: {result.stderr}"
        assert 'CCC Alpha (cca)' in result.stdout, "Version output incorrect"
    
    def test_help(self):
        """Test cca --help"""
        result = subprocess.run(['cca', '--help'], capture_output=True, text=True)
        assert result.returncode == 0, f"--help failed: {result.stderr}"
        assert 'CCC Alpha - Minimal CCC CODE Tools' in result.stdout
    
    def test_info_command(self):
        """Test cca info"""
        result = subprocess.run(['cca', 'info'], capture_output=True, text=True)
        assert result.returncode == 0, f"info command failed: {result.stderr}"
        assert 'CCC Alpha (cca)' in result.stdout, "Info output incorrect"
        assert 'Available commands' in result.stdout, "Commands list missing"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
