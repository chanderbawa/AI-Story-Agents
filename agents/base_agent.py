"""
Base Agent Class
Provides common functionality for all AI agents in the story creation system.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)


class Message:
    """Message object for inter-agent communication."""
    
    def __init__(self, sender: str, recipient: str, content: Dict[str, Any], 
                 message_type: str = "info"):
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.message_type = message_type  # info, request, response, error
        self.timestamp = datetime.now()
        self.id = f"{sender}_{recipient}_{self.timestamp.timestamp()}"
    
    def __repr__(self):
        return f"Message({self.sender} → {self.recipient}: {self.message_type})"


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the story creation system.
    
    Each agent has:
    - Unique name and role
    - Memory of past interactions
    - Ability to send/receive messages
    - Specialized capabilities
    """
    
    def __init__(self, name: str, role: str, config: Dict[str, Any]):
        self.name = name
        self.role = role
        self.config = config
        self.memory: List[Message] = []
        self.logger = logging.getLogger(f"Agent.{name}")
        self.status = "idle"  # idle, working, waiting, error
        
        self.logger.info(f"🤖 {name} ({role}) initialized")
    
    @abstractmethod
    def process_message(self, message: Message) -> Optional[Message]:
        """
        Process an incoming message and optionally return a response.
        
        Args:
            message: Incoming message from another agent
            
        Returns:
            Optional response message
        """
        pass
    
    @abstractmethod
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a specific task assigned to this agent.
        
        Args:
            task: Task specification with required parameters
            
        Returns:
            Task results
        """
        pass
    
    def send_message(self, recipient: str, content: Dict[str, Any], 
                    message_type: str = "info") -> Message:
        """Create and log a message to another agent."""
        message = Message(self.name, recipient, content, message_type)
        self.memory.append(message)
        self.logger.info(f"📤 Sent {message_type} to {recipient}")
        return message
    
    def receive_message(self, message: Message):
        """Receive and store a message."""
        self.memory.append(message)
        self.logger.info(f"📥 Received {message.message_type} from {message.sender}")
        return self.process_message(message)
    
    def get_context(self, limit: int = 10) -> List[Message]:
        """Get recent message history for context."""
        return self.memory[-limit:]
    
    def update_status(self, status: str, details: str = ""):
        """Update agent status."""
        self.status = status
        self.logger.info(f"Status: {status} {details}")
    
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities."""
        return []
    
    def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if agent can handle the given task."""
        return True
    
    def __repr__(self):
        return f"{self.name} ({self.role}) - {self.status}"
