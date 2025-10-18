"""Test CCB Check Plugin"""
import subprocess
import pytest


class TestCCBCheck:
    """Test ccb check commands"""
    
    def test_check_actions_command_exists(self):
        """Test if check actions command exists"""
        result = subprocess.run(
            ['ccb', 'check', 'actions', '--help'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert 'GitHub Actions' in result.stdout or 'workflow' in result.stdout
    
    def test_check_actions_save_flag(self):
        """Test check actions --save flag"""
        # Nur wenn gh CLI verfügbar
        gh_check = subprocess.run(['which', 'gh'], capture_output=True)
        if gh_check.returncode != 0:
            pytest.skip("gh CLI not installed")
        
        result = subprocess.run(
            ['ccb', 'check', 'actions', '--save'],
            capture_output=True,
            text=True
        )
        # Command sollte ausführbar sein (auch wenn GitHub API Probleme hat)
        assert 'invalid choice' not in result.stderr


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
