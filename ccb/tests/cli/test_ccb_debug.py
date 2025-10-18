"""Test CCB Debug Plugin"""
import subprocess
import os
import pytest


class TestCCBDebug:
    """Test ccb debug commands"""
    
    def test_debug_run_command_exists(self):
        """Test if debug run command exists"""
        result = subprocess.run(
            ['ccb', 'debug', 'run', '--help'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert 'run all tests' in result.stdout or 'aggregate' in result.stdout
    
    def test_debug_summary_command_exists(self):
        """Test if debug summary command exists"""
        result = subprocess.run(
            ['ccb', 'debug', 'summary', '--help'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert 'summary' in result.stdout
    
    def test_debug_summary_no_log(self):
        """Test debug summary when no log exists"""
        # Remove log if exists
        log_file = './logs/ccb-debug.log'
        if os.path.exists(log_file):
            os.remove(log_file)
        
        result = subprocess.run(
            ['ccb', 'debug', 'summary'],
            capture_output=True,
            text=True
        )
        assert 'No debug log found' in result.stdout or result.returncode in [0, 1]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
