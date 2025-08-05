#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the SystemInfoReader module
"""

import unittest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock
import sys

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from system_info_reader import SystemInfoReader


class TestSystemInfoReader(unittest.TestCase):
    """Test cases for SystemInfoReader class"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.reader = SystemInfoReader()

    def test_init(self):
        """Test SystemInfoReader initialization"""
        reader = SystemInfoReader()
        self.assertIsInstance(reader.info, dict)
        self.assertEqual(len(reader.info), 0)

    @patch('system_info_reader.platform')
    @patch('system_info_reader.psutil')
    def test_get_system_info(self, mock_psutil, mock_platform):
        """Test system information collection"""
        # Mock platform module
        mock_platform.system.return_value = 'Linux'
        mock_platform.version.return_value = '5.4.0'
        mock_platform.release.return_value = '20.04'
        mock_platform.architecture.return_value = ('64bit', 'ELF')
        mock_platform.machine.return_value = 'x86_64'
        mock_platform.processor.return_value = 'x86_64'
        mock_platform.node.return_value = 'test-host'

        # Mock psutil
        mock_psutil.boot_time.return_value = 1609459200  # 2021-01-01

        self.reader.get_system_info()

        self.assertIn('system', self.reader.info)
        self.assertEqual(self.reader.info['system']['os'], 'Linux')
        self.assertEqual(self.reader.info['system']['hostname'], 'test-host')
        self.assertIn('timestamp', self.reader.info['system'])

    @patch('system_info_reader.psutil')
    def test_get_hardware_info(self, mock_psutil):
        """Test hardware information collection"""
        # Mock CPU info
        mock_psutil.cpu_count.return_value = 4
        mock_cpu_freq = MagicMock()
        mock_cpu_freq._asdict.return_value = {'current': 2400, 'min': 1200, 'max': 3600}
        mock_psutil.cpu_freq.return_value = mock_cpu_freq

        # Mock memory info
        mock_memory = MagicMock()
        mock_memory.total = 8589934592  # 8GB
        mock_memory.available = 4294967296  # 4GB
        mock_memory.percent = 50.0
        mock_psutil.virtual_memory.return_value = mock_memory

        # Mock disk info
        mock_partition = MagicMock()
        mock_partition.device = '/dev/sda1'
        mock_partition.mountpoint = '/'
        mock_partition.fstype = 'ext4'
        mock_psutil.disk_partitions.return_value = [mock_partition]

        mock_usage = MagicMock()
        mock_usage.total = 1000000000000  # 1TB
        mock_usage.used = 500000000000   # 500GB
        mock_usage.free = 500000000000   # 500GB
        mock_psutil.disk_usage.return_value = mock_usage

        self.reader.get_hardware_info()

        self.assertIn('hardware', self.reader.info)
        self.assertEqual(self.reader.info['hardware']['cpu_count'], 4)
        self.assertIn('memory', self.reader.info['hardware'])
        self.assertEqual(self.reader.info['hardware']['memory']['total'], 8589934592)
        self.assertIn('disk_usage', self.reader.info['hardware'])
        self.assertEqual(len(self.reader.info['hardware']['disk_usage']), 1)

    @patch('system_info_reader.platform.system')
    def test_get_installed_programs_linux(self, mock_system):
        """Test Linux program collection"""
        mock_system.return_value = 'Linux'

        with patch('system_info_reader.subprocess.run') as mock_run:
            # Mock successful dpkg command
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "ii  python3  3.8.10  Python interpreter"
            mock_run.return_value = mock_result

            self.reader.get_installed_programs()

            self.assertIn('programs', self.reader.info)
            self.assertIsInstance(self.reader.info['programs'], list)

    @patch('system_info_reader.platform.system')
    def test_get_installed_programs_mac(self, mock_system):
        """Test macOS program collection"""
        mock_system.return_value = 'Darwin'

        with patch('system_info_reader.Path') as mock_path:
            # Mock Applications directory
            mock_apps_path = MagicMock()
            mock_apps_path.exists.return_value = True
            mock_app = MagicMock()
            mock_app.name = 'TestApp.app'
            mock_apps_path.glob.return_value = [mock_app]
            mock_path.return_value = mock_apps_path

            self.reader.get_installed_programs()

            self.assertIn('programs', self.reader.info)
            self.assertIsInstance(self.reader.info['programs'], list)

    @patch('system_info_reader.psutil')
    def test_get_network_info(self, mock_psutil):
        """Test network information collection"""
        # Mock network interfaces
        mock_addr = MagicMock()
        mock_addr.family = 2  # AF_INET
        mock_addr.address = '192.168.1.100'

        mock_psutil.net_if_addrs.return_value = {
            'eth0': [mock_addr],
            'lo': [mock_addr]
        }

        self.reader.get_network_info()

        self.assertIn('network', self.reader.info)
        self.assertIn('interfaces', self.reader.info['network'])
        self.assertEqual(len(self.reader.info['network']['interfaces']), 2)

    @patch('system_info_reader.psutil')
    def test_get_running_processes(self, mock_psutil):
        """Test running processes collection"""
        # Mock process list
        mock_proc1 = MagicMock()
        mock_proc1.info = {'name': 'python', 'cpu_percent': 25.5}
        mock_proc2 = MagicMock()
        mock_proc2.info = {'name': 'bash', 'cpu_percent': 0.1}

        mock_psutil.process_iter.return_value = [mock_proc1, mock_proc2]

        self.reader.get_running_processes()

        self.assertIn('processes', self.reader.info)
        self.assertIsInstance(self.reader.info['processes'], list)
        self.assertLessEqual(len(self.reader.info['processes']), 20)  # Should limit to top 20
        # Should be sorted by CPU usage (highest first)
        if len(self.reader.info['processes']) > 1:
            self.assertGreaterEqual(
                self.reader.info['processes'][0]['cpu_percent'],
                self.reader.info['processes'][1]['cpu_percent']
            )

    def test_collect_all_info(self):
        """Test collecting all information"""
        with patch.object(self.reader, 'get_system_info') as mock_system, \
             patch.object(self.reader, 'get_hardware_info') as mock_hardware, \
             patch.object(self.reader, 'get_installed_programs') as mock_programs, \
             patch.object(self.reader, 'get_network_info') as mock_network, \
             patch.object(self.reader, 'get_running_processes') as mock_processes:

            result = self.reader.collect_all_info()

            # Verify all methods were called
            mock_system.assert_called_once()
            mock_hardware.assert_called_once()
            mock_programs.assert_called_once()
            mock_network.assert_called_once()
            mock_processes.assert_called_once()

            # Should return the info dict
            self.assertEqual(result, self.reader.info)

    def test_save_to_file(self):
        """Test saving information to JSON file"""
        # Add some test data
        self.reader.info = {'test': 'data', 'number': 42}

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
            tmp_filename = tmp_file.name

        try:
            self.reader.save_to_file(tmp_filename)

            # Verify file was created and contains correct data
            self.assertTrue(os.path.exists(tmp_filename))

            with open(tmp_filename, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)

            self.assertEqual(saved_data, self.reader.info)

        finally:
            # Clean up
            if os.path.exists(tmp_filename):
                os.unlink(tmp_filename)

    @patch('system_info_reader.requests.post')
    def test_send_to_claude_success(self, mock_post):
        """Test successful Claude API communication"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'content': [{'text': 'Your system looks good!'}]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        self.reader.info = {'test': 'data'}
        result = self.reader.send_to_claude('test-api-key', 'Analyze my system')

        self.assertEqual(result, 'Your system looks good!')
        mock_post.assert_called_once()

    @patch('system_info_reader.requests.post')
    def test_send_to_claude_error(self, mock_post):
        """Test Claude API communication error"""
        # Mock API error - using requests.exceptions.RequestException
        from requests.exceptions import RequestException
        mock_post.side_effect = RequestException('API Error')

        self.reader.info = {'test': 'data'}
        result = self.reader.send_to_claude('test-api-key', 'Analyze my system')

        self.assertIsNone(result)

    def test_send_to_claude_large_data(self):
        """Test Claude API with large data that needs summarization"""
        # Create large data that exceeds 50KB limit
        large_data = {'large_field': 'x' * 60000}
        self.reader.info = large_data

        with patch('system_info_reader.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'content': [{'text': 'Summarized analysis'}]
            }
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response

            result = self.reader.send_to_claude('test-api-key')

            # Should have summarized the data
            self.assertEqual(result, 'Summarized analysis')
            # Check that the posted data was summarized
            call_args = mock_post.call_args
            posted_data = call_args[1]['json']
            self.assertIn('note', posted_data['messages'][0]['content'])


class TestScriptExecution(unittest.TestCase):
    """Test script execution and CLI functionality"""

    def test_import_module(self):
        """Test that the module can be imported without errors"""
        import system_info_reader
        self.assertTrue(hasattr(system_info_reader, 'SystemInfoReader'))
        self.assertTrue(hasattr(system_info_reader, 'main'))

    def test_module_has_required_dependencies(self):
        """Test that required dependencies are available"""
        try:
            import psutil  # noqa: F401
            import requests  # noqa: F401
            self.assertTrue(True)  # Dependencies available
        except ImportError:
            self.fail("Required dependencies not available")

    def test_cli_help(self):
        """Test CLI help functionality"""
        import subprocess
        result = subprocess.run(
            [sys.executable, 'system_info_reader.py', '--help'],
            capture_output=True, text=True, cwd=os.path.dirname(__file__) + '/..'
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn('Coletor de Informações do Sistema', result.stdout)

    def test_cli_summary(self):
        """Test CLI summary functionality"""
        import subprocess
        result = subprocess.run(
            [sys.executable, 'system_info_reader.py', '--summary'],
            capture_output=True, text=True, cwd=os.path.dirname(__file__) + '/..',
            timeout=60
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn('RESUMO DO SISTEMA', result.stdout)
        self.assertIn('OS:', result.stdout)
        self.assertIn('CPU:', result.stdout)

    def test_cli_save_quiet(self):
        """Test CLI save functionality in quiet mode"""
        import subprocess
        import tempfile

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
            tmp_filename = tmp_file.name

        try:
            result = subprocess.run(
                [sys.executable, 'system_info_reader.py', '--save', tmp_filename, '--quiet'],
                capture_output=True, text=True, cwd=os.path.dirname(__file__) + '/..',
                timeout=60
            )
            self.assertEqual(result.returncode, 0)

            # Verify file was created and contains valid JSON
            self.assertTrue(os.path.exists(tmp_filename))
            with open(tmp_filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.assertIn('system', data)
            self.assertIn('hardware', data)

        finally:
            # Clean up
            if os.path.exists(tmp_filename):
                os.unlink(tmp_filename)


if __name__ == '__main__':
    unittest.main()
