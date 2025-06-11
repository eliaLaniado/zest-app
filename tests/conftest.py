import pytest
from unittest.mock import MagicMock
from app.models.tasks import Task
from uuid import uuid4

@pytest.fixture
def sample_task():
    """Return a sample Task instance for testing."""
    return Task(id=uuid4(), message="test", attempts=0)

@pytest.fixture
def mock_logger():
    """Return a MagicMock logger."""
    return MagicMock()

@pytest.fixture
def mock_metrics():
    """Return a MagicMock metrics object."""
    return MagicMock()

@pytest.fixture
def mock_queue():
    """Return a MagicMock queue object."""
    return MagicMock()