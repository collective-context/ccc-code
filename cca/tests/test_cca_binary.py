"""Test CCA Binary"""
import subprocess
import pytest


class TestCCABinary:
    """Test CCA binary availability and execution"""
    
    def test_binary_exists(self):
        """Test if cca binary exists in PATH"""
        result = subprocess.run(['which', 'cca'], capture_output=True)
        assert result.returncode == 0, "cca binary not found in PATH"
    
    def test_binary_executable(self):
        """Test if cca binary is executable"""
        result = subprocess.run(['cca', '--version'], capture_output=True, text=True)
        assert result.returncode == 0, f"cca binary not executable: {result.stderr}"
    
    def test_python_package_import(self):
        """Test if Python package can be imported"""
        result = subprocess.run(
            ['python3', '-c', 'import cca; print(cca.__version__)'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Cannot import cca package: {result.stderr}"
        assert '0.1.0' in result.stdout, "Version mismatch"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
