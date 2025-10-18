"""Test CCA base commands"""

import subprocess
import pytest


def test_cca_version():
    """Test cca --version command"""
    result = subprocess.run(
        ['cca', '--version'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'CCC Alpha (cca)' in result.stdout
    assert 'v0.1.0' in result.stdout


def test_cca_help():
    """Test cca --help command"""
    result = subprocess.run(
        ['cca', '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'usage:' in result.stdout.lower()


def test_cca_info():
    """Test cca info command"""
    result = subprocess.run(
        ['cca', 'info'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'CCC Alpha (cca)' in result.stdout
    assert 'Available commands:' in result.stdout


def test_cca_check_help():
    """Test cca check --help command"""
    result = subprocess.run(
        ['cca', 'check', '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'usage:' in result.stdout.lower()


def test_cca_debug_help():
    """Test cca debug --help command"""
    result = subprocess.run(
        ['cca', 'debug', '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'usage:' in result.stdout.lower()


def test_cca_debug_run_help():
    """Test cca debug run --help command"""
    result = subprocess.run(
        ['cca', 'debug', 'run', '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'usage:' in result.stdout.lower()


def test_cca_debug_summary_help():
    """Test cca debug summary --help command"""
    result = subprocess.run(
        ['cca', 'debug', 'summary', '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'usage:' in result.stdout.lower()


def test_cca_check_actions_help():
    """Test cca check actions --help command"""
    result = subprocess.run(
        ['cca', 'check', 'actions', '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'usage:' in result.stdout.lower()
