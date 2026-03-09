"""
Unit Tests for Workflow Utility Scripts
"""

import pytest
import json
from pathlib import Path
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from workflow_validator import WorkflowValidator
from backup_workflows import WorkflowBackup


class TestWorkflowValidator:
    """Tests for workflow validator"""
    
    def test_validate_json_structure(self, tmp_path):
        """Test JSON structure validation"""
        validator = WorkflowValidator()
        
        # Valid JSON
        valid_file = tmp_path / "valid.json"
        valid_file.write_text('{"id": "123", "name": "Test", "nodes": []}')
        
        is_valid, data = validator.validate_json_structure(valid_file)
        assert is_valid is True
        assert data is not None
        
        # Invalid JSON
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text('{"invalid json}')
        
        is_valid, data = validator.validate_json_structure(invalid_file)
        assert is_valid is False
        assert data is None
    
    def test_validate_required_fields(self):
        """Test required fields validation"""
        validator = WorkflowValidator()
        
        # Valid workflow
        valid_data = {
            "id": "test-123",
            "name": "Test Workflow",
            "nodes": []
        }
        assert validator.validate_required_fields(valid_data) is True
        
        # Missing required field
        invalid_data = {
            "id": "test-123",
            "name": "Test Workflow"
        }
        assert validator.validate_required_fields(invalid_data) is False
    
    def test_check_nodes(self):
        """Test node analysis"""
        validator = WorkflowValidator()
        
        data = {
            "nodes": [
                {
                    "id": "node1",
                    "name": "Start",
                    "type": "n8n-nodes-base.start"
                },
                {
                    "id": "node2",
                    "name": "HTTP Request",
                    "type": "n8n-nodes-base.httpRequest",
                    "credentials": {
                        "httpApiKey": {"id": "123", "name": "My API"}
                    }
                }
            ]
        }
        
        stats = validator.check_nodes(data)
        
        assert stats['total_nodes'] == 2
        assert 'n8n-nodes-base.start' in stats['node_types']
        assert 'httpApiKey' in stats['credentials_needed']


class TestWorkflowBackup:
    """Tests for workflow backup manager"""
    
    def test_create_backup(self, tmp_path):
        """Test backup creation"""
        # Create test workflows directory
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir()
        
        # Create test workflow
        test_workflow = workflows_dir / "test.json"
        test_workflow.write_text('{"id": "1", "name": "Test"}')
        
        # Create backup
        backup_dir = tmp_path / "backups"
        backup_manager = WorkflowBackup(str(workflows_dir), str(backup_dir))
        
        backup_path = backup_manager.create_backup("test backup")
        
        assert backup_path is not None
        assert backup_path.exists()
        assert (backup_path / "test.json").exists()
        assert (backup_path / "backup_metadata.json").exists()
    
    def test_list_backups(self, tmp_path):
        """Test listing backups"""
        workflows_dir = tmp_path / "workflows"
        workflows_dir.mkdir()
        
        backup_dir = tmp_path / "backups"
        backup_manager = WorkflowBackup(str(workflows_dir), str(backup_dir))
        
        # Create test backups
        backup_manager.create_backup("first")
        backup_manager.create_backup("second")
        
        backups = backup_manager.list_backups()
        
        assert len(backups) == 2
        assert all('timestamp' in b for b in backups)
        assert all('description' in b for b in backups)


def test_environment_file_exists():
    """Test that .env.example exists"""
    env_example = Path(__file__).parent.parent / ".env.example"
    assert env_example.exists()


def test_package_json_valid():
    """Test that package.json is valid"""
    package_json = Path(__file__).parent.parent / "package.json"
    assert package_json.exists()
    
    with open(package_json) as f:
        data = json.load(f)
    
    assert 'name' in data
    assert 'version' in data
    assert 'scripts' in data


def test_requirements_file_exists():
    """Test that requirements.txt exists"""
    requirements = Path(__file__).parent.parent / "requirements.txt"
    assert requirements.exists()
    
    content = requirements.read_text()
    assert 'python-dotenv' in content
    assert 'requests' in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
