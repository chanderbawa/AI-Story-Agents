"""
Message Broker for Distributed Agent Communication
Handles async messaging between independent agent services
"""

import json
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from pathlib import Path
import threading
import queue
import time

logger = logging.getLogger(__name__)


class Message:
    """Message format for inter-agent communication"""
    
    def __init__(
        self,
        message_id: str,
        sender: str,
        receiver: str,
        message_type: str,
        content: Dict[str, Any],
        correlation_id: Optional[str] = None
    ):
        self.message_id = message_id
        self.sender = sender
        self.receiver = receiver
        self.message_type = message_type
        self.content = content
        self.correlation_id = correlation_id or message_id
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'message_id': self.message_id,
            'sender': self.sender,
            'receiver': self.receiver,
            'message_type': self.message_type,
            'content': self.content,
            'correlation_id': self.correlation_id,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        msg = cls(
            message_id=data['message_id'],
            sender=data['sender'],
            receiver=data['receiver'],
            message_type=data['message_type'],
            content=data['content'],
            correlation_id=data.get('correlation_id')
        )
        msg.timestamp = data.get('timestamp', datetime.now().isoformat())
        return msg


class MessageBroker:
    """
    Simple in-memory message broker for agent communication.
    
    In production, replace with RabbitMQ, Redis, or Kafka.
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.queues: Dict[str, queue.Queue] = {}
        self.subscribers: Dict[str, list] = {}
        self.message_history: list = []
        self.storage_path = storage_path or Path("output/messages")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        
        logger.info("📬 Message Broker initialized")
    
    def create_queue(self, queue_name: str):
        """Create a message queue for an agent"""
        if queue_name not in self.queues:
            self.queues[queue_name] = queue.Queue()
            logger.info(f"📫 Created queue: {queue_name}")
    
    def publish(self, message: Message):
        """Publish a message to the receiver's queue"""
        with self.lock:
            receiver = message.receiver
            
            # Create queue if doesn't exist
            if receiver not in self.queues:
                self.create_queue(receiver)
            
            # Add to queue
            self.queues[receiver].put(message)
            
            # Store in history
            self.message_history.append(message)
            
            # Persist to disk
            self._save_message(message)
            
            logger.info(
                f"📨 Message sent: {message.sender} → {message.receiver} "
                f"({message.message_type})"
            )
            
            # Notify subscribers
            if receiver in self.subscribers:
                for callback in self.subscribers[receiver]:
                    threading.Thread(
                        target=callback,
                        args=(message,),
                        daemon=True
                    ).start()
    
    def subscribe(self, agent_name: str, callback: Callable):
        """Subscribe to messages for an agent"""
        if agent_name not in self.subscribers:
            self.subscribers[agent_name] = []
        self.subscribers[agent_name].append(callback)
        logger.info(f"🔔 {agent_name} subscribed to messages")
    
    def receive(self, agent_name: str, timeout: Optional[float] = None) -> Optional[Message]:
        """Receive a message from agent's queue"""
        if agent_name not in self.queues:
            self.create_queue(agent_name)
        
        try:
            message = self.queues[agent_name].get(timeout=timeout)
            logger.info(
                f"📬 Message received by {agent_name}: "
                f"{message.sender} ({message.message_type})"
            )
            return message
        except queue.Empty:
            return None
    
    def get_messages_by_correlation(self, correlation_id: str) -> list:
        """Get all messages in a conversation"""
        return [
            msg for msg in self.message_history
            if msg.correlation_id == correlation_id
        ]
    
    def _save_message(self, message: Message):
        """Persist message to disk"""
        try:
            filepath = self.storage_path / f"{message.message_id}.json"
            with open(filepath, 'w') as f:
                json.dump(message.to_dict(), f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save message: {e}")
    
    def clear_queue(self, agent_name: str):
        """Clear all messages in an agent's queue"""
        if agent_name in self.queues:
            while not self.queues[agent_name].empty():
                try:
                    self.queues[agent_name].get_nowait()
                except queue.Empty:
                    break
            logger.info(f"🗑️  Cleared queue: {agent_name}")


class RedisMessageBroker(MessageBroker):
    """
    Redis-based message broker for production use.
    Supports distributed deployment across multiple servers.
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        super().__init__()
        try:
            import redis
            self.redis_client = redis.from_url(redis_url)
            self.pubsub = self.redis_client.pubsub()
            logger.info(f"📬 Redis Message Broker connected: {redis_url}")
        except ImportError:
            logger.warning("Redis not installed. Install with: pip install redis")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    def publish(self, message: Message):
        """Publish message to Redis"""
        channel = f"agent:{message.receiver}"
        self.redis_client.publish(channel, json.dumps(message.to_dict()))
        
        # Store in history
        self.redis_client.lpush(
            f"history:{message.correlation_id}",
            json.dumps(message.to_dict())
        )
        
        logger.info(f"📨 Redis: {message.sender} → {message.receiver}")
    
    def subscribe(self, agent_name: str, callback: Callable):
        """Subscribe to Redis channel"""
        channel = f"agent:{agent_name}"
        self.pubsub.subscribe(**{channel: lambda msg: callback(
            Message.from_dict(json.loads(msg['data']))
        )})
        
        # Start listening thread
        thread = self.pubsub.run_in_thread(sleep_time=0.1)
        logger.info(f"🔔 Redis: {agent_name} subscribed")
        return thread


# Singleton instance
_broker_instance: Optional[MessageBroker] = None


def get_broker(broker_type: str = "memory", **kwargs) -> MessageBroker:
    """Get or create message broker instance"""
    global _broker_instance
    
    if _broker_instance is None:
        if broker_type == "redis":
            _broker_instance = RedisMessageBroker(**kwargs)
        else:
            _broker_instance = MessageBroker(**kwargs)
    
    return _broker_instance
