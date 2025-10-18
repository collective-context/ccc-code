"""Test CCA Installation"""
import subprocess
import os
import pytest


class TestCCAInstall:
    """Test CCA installation process"""
    
    def test_cleanup_old_installation(self):
        """Test cleanup of previous CCA installation"""
                
        result = subprocess.run(
            ['sudo', 'rm', '-rf', 
             '/root/caa', '/opt/caa', '/etc/caa', '/var/log/cca', 
             '/usr/local/bin/cca', '/usr/bin/cca', '/tmp/caa', '/tmp/ccc-code'],
            capture_output=True
        )
        assert result.returncode == 0, "Cleanup failed"
    
    def test_run_installer(self):
        """Test CCA installer script"""
        result = subprocess.run(
            ['sudo', '-E', 'bash', 'install-cca'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Installation failed: {result.stderr}"
        assert "Installation complete" in result.stdout, "Installation did not complete successfully"
    
    def test_virtual_env_created(self):
        """Test if virtual environment was created"""
        assert os.path.exists('/opt/cca'), "Virtual environment directory not found"
        assert os.path.exists('/opt/cca/bin/cca'), "CCA binary not found in venv"
    
    def test_symlinks_created(self):
        """Test if symlinks were created"""
        assert os.path.islink('/usr/local/bin/cca'), "Symlink /usr/local/bin/cca not found"
        assert os.path.islink('/usr/bin/cca'), "Symlink /usr/bin/cca not found"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
