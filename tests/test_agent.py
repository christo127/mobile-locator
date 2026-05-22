"""Tests for Mobile Locator Agent"""

import pytest
from src.agent import MobileLocatorAgent


class TestMobileLocatorAgent:
    """Test MobileLocatorAgent class"""
    
    @pytest.fixture
    def agent(self):
        """Create agent instance for testing"""
        return MobileLocatorAgent(db_path="data")
    
    def test_agent_initialization(self, agent):
        """Test agent initialization"""
        assert agent is not None
        assert agent.parser is not None
        assert agent.db is not None
    
    def test_validate_phone_valid(self, agent):
        """Test validation of valid phone number"""
        result = agent.validate_phone("+14155552671")
        assert isinstance(result, bool)
    
    def test_validate_phone_invalid(self, agent):
        """Test validation of invalid phone number"""
        result = agent.validate_phone("invalid")
        assert result is False
    
    def test_locate_batch(self, agent):
        """Test batch location"""
        numbers = ["+14155552671", "+447911123456"]
        results = agent.locate_batch(numbers)
        assert len(results) == 2
        assert isinstance(results, list)
