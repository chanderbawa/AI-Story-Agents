"""
Distributed Orchestrator - Coordinates distributed agents
"""

import logging
import uuid
import time
from typing import Dict, Any, Optional
from .message_broker import MessageBroker, Message, get_broker

logger = logging.getLogger(__name__)


class DistributedOrchestrator:
    """
    Orchestrates story creation using distributed agent services.
    Agents can run on separate machines/containers.
    """
    
    def __init__(self, broker: Optional[MessageBroker] = None):
        self.broker = broker or get_broker()
        self.broker.create_queue('Orchestrator')
        self.pending_tasks: Dict[str, Dict[str, Any]] = {}
        
        logger.info("🎬 Distributed Orchestrator initialized")
    
    def create_story(
        self,
        story_idea: Dict[str, Any],
        timeout: int = 1800  # 30 minutes
    ) -> Dict[str, Any]:
        """
        Create a story using distributed agents.
        
        Workflow:
        1. Send request to Author Service
        2. Author creates story → sends to Illustrator
        3. Illustrator creates images → sends to Publisher
        4. Publisher creates PDF → sends result back
        """
        
        correlation_id = str(uuid.uuid4())
        
        logger.info(f"📖 Starting distributed story creation: {correlation_id}")
        logger.info(f"Plot: {story_idea.get('plot', '')[:100]}...")
        
        # Track task
        self.pending_tasks[correlation_id] = {
            'status': 'started',
            'start_time': time.time(),
            'story_idea': story_idea
        }
        
        # Send initial request to Author Service
        message = Message(
            message_id=str(uuid.uuid4()),
            sender='Orchestrator',
            receiver='AuthorService',
            message_type='request',
            content={
                'action': 'create_story',
                **story_idea
            },
            correlation_id=correlation_id
        )
        
        self.broker.publish(message)
        
        logger.info("📨 Request sent to Author Service")
        logger.info("⏳ Waiting for completion...")
        
        # Wait for completion
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Check for response
            response = self.broker.receive('Orchestrator', timeout=1.0)
            
            if response and response.correlation_id == correlation_id:
                if response.content.get('action') == 'complete':
                    logger.info("✅ Story creation complete!")
                    
                    result = response.content.get('result', {})
                    result['status'] = 'complete'
                    result['correlation_id'] = correlation_id
                    
                    # Cleanup
                    del self.pending_tasks[correlation_id]
                    
                    return result
                
                elif response.content.get('action') == 'error':
                    logger.error(f"❌ Error: {response.content.get('error')}")
                    return {
                        'status': 'error',
                        'message': response.content.get('error'),
                        'correlation_id': correlation_id
                    }
                
                else:
                    # Progress update
                    logger.info(
                        f"📊 Progress: {response.sender} → "
                        f"{response.content.get('action', 'processing')}"
                    )
        
        # Timeout
        logger.error(f"⏱️ Timeout after {timeout} seconds")
        return {
            'status': 'timeout',
            'message': f'Story creation timed out after {timeout} seconds',
            'correlation_id': correlation_id
        }
    
    def get_task_status(self, correlation_id: str) -> Dict[str, Any]:
        """Get status of a task"""
        if correlation_id in self.pending_tasks:
            task = self.pending_tasks[correlation_id]
            elapsed = time.time() - task['start_time']
            return {
                'correlation_id': correlation_id,
                'status': task['status'],
                'elapsed_seconds': int(elapsed)
            }
        else:
            # Check message history
            messages = self.broker.get_messages_by_correlation(correlation_id)
            if messages:
                latest = messages[-1]
                return {
                    'correlation_id': correlation_id,
                    'status': 'completed' if latest.receiver == 'Orchestrator' else 'in_progress',
                    'latest_agent': latest.receiver
                }
            else:
                return {
                    'correlation_id': correlation_id,
                    'status': 'not_found'
                }
    
    def get_message_history(self, correlation_id: str) -> list:
        """Get all messages for a task"""
        messages = self.broker.get_messages_by_correlation(correlation_id)
        return [msg.to_dict() for msg in messages]
