"""
Agent Service - Wraps agents to run as independent services
"""

import logging
import threading
import time
import uuid
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from .message_broker import MessageBroker, Message, get_broker

logger = logging.getLogger(__name__)


class AgentService:
    """
    Wrapper to run an agent as an independent service.
    Can be deployed separately and communicate via message broker.
    """
    
    def __init__(
        self,
        agent,
        agent_name: str,
        port: int,
        broker: Optional[MessageBroker] = None
    ):
        self.agent = agent
        self.agent_name = agent_name
        self.port = port
        self.broker = broker or get_broker()
        self.app = Flask(f"{agent_name}_service")
        self.running = False
        self.worker_thread = None
        
        # Create queue for this agent
        self.broker.create_queue(agent_name)
        
        # Setup Flask routes
        self._setup_routes()
        
        logger.info(f"🚀 {agent_name} Service initialized on port {port}")
    
    def _setup_routes(self):
        """Setup REST API endpoints"""
        
        @self.app.route('/health', methods=['GET'])
        def health():
            return jsonify({
                'status': 'healthy',
                'agent': self.agent_name,
                'agent_status': self.agent.status
            })
        
        @self.app.route('/send', methods=['POST'])
        def send_message():
            """Send a message to this agent"""
            data = request.json
            
            message = Message(
                message_id=str(uuid.uuid4()),
                sender=data.get('sender', 'external'),
                receiver=self.agent_name,
                message_type=data.get('message_type', 'request'),
                content=data.get('content', {}),
                correlation_id=data.get('correlation_id')
            )
            
            self.broker.publish(message)
            
            return jsonify({
                'status': 'accepted',
                'message_id': message.message_id
            })
        
        @self.app.route('/status', methods=['GET'])
        def status():
            """Get agent status"""
            return jsonify({
                'agent': self.agent_name,
                'status': self.agent.status,
                'state': self.agent.state
            })
    
    def start(self, background: bool = True):
        """Start the agent service"""
        self.running = True
        
        # Start message processing worker
        self.worker_thread = threading.Thread(
            target=self._process_messages,
            daemon=True
        )
        self.worker_thread.start()
        
        logger.info(f"✅ {self.agent_name} Service started")
        
        if background:
            # Run Flask in background thread
            threading.Thread(
                target=lambda: self.app.run(
                    host='0.0.0.0',
                    port=self.port,
                    debug=False,
                    use_reloader=False
                ),
                daemon=True
            ).start()
        else:
            # Run Flask in main thread (blocking)
            self.app.run(
                host='0.0.0.0',
                port=self.port,
                debug=False
            )
    
    def stop(self):
        """Stop the agent service"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        logger.info(f"🛑 {self.agent_name} Service stopped")
    
    def _process_messages(self):
        """Worker thread to process incoming messages"""
        logger.info(f"👂 {self.agent_name} listening for messages...")
        
        while self.running:
            try:
                # Receive message from broker
                message = self.broker.receive(self.agent_name, timeout=1.0)
                
                if message:
                    logger.info(
                        f"📨 {self.agent_name} processing message from "
                        f"{message.sender}"
                    )
                    
                    # Process message with agent
                    response = self._handle_message(message)
                    
                    # Send response if needed
                    if response:
                        response_msg = Message(
                            message_id=str(uuid.uuid4()),
                            sender=self.agent_name,
                            receiver=response.get('receiver', message.sender),
                            message_type='response',
                            content=response,
                            correlation_id=message.correlation_id
                        )
                        self.broker.publish(response_msg)
                        
            except Exception as e:
                logger.error(f"Error processing message: {e}", exc_info=True)
                time.sleep(1)
    
    def _handle_message(self, message: Message) -> Optional[Dict[str, Any]]:
        """Handle incoming message based on agent type"""
        
        content = message.content
        action = content.get('action')
        
        if not action:
            logger.warning(f"No action specified in message: {message.message_id}")
            return None
        
        try:
            # Route to appropriate agent method
            if action == 'create_story':
                result = self.agent.execute_task(content)
                return {
                    'receiver': 'IllustratorService',  # Next in pipeline
                    'action': 'generate_illustrations',
                    'story_data': result,
                    'correlation_id': message.correlation_id
                }
            
            elif action == 'generate_illustrations':
                result = self.agent.execute_task(content)
                return {
                    'receiver': 'PublisherService',  # Next in pipeline
                    'action': 'create_publication',
                    'story_data': content.get('story_data'),
                    'illustrations': result,
                    'correlation_id': message.correlation_id
                }
            
            elif action == 'create_publication':
                result = self.agent.execute_task(content)
                return {
                    'receiver': 'Orchestrator',  # Back to orchestrator
                    'action': 'complete',
                    'result': result,
                    'correlation_id': message.correlation_id
                }
            
            else:
                logger.warning(f"Unknown action: {action}")
                return None
                
        except Exception as e:
            logger.error(f"Error executing {action}: {e}", exc_info=True)
            return {
                'receiver': message.sender,
                'action': 'error',
                'error': str(e),
                'correlation_id': message.correlation_id
            }


def run_author_service(port: int = 8001, config_path: str = None):
    """Run Author Agent as a service"""
    from agents.author_agent import AuthorAgent
    import yaml
    
    # Load config
    if config_path:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {}
    
    # Create agent
    agent = AuthorAgent(config.get('author', {}))
    
    # Create service
    service = AgentService(agent, 'AuthorService', port)
    service.start(background=False)


def run_illustrator_service(port: int = 8002, config_path: str = None):
    """Run Illustrator Agent as a service"""
    from agents.illustrator_agent import IllustratorAgent
    import yaml
    
    if config_path:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {}
    
    agent = IllustratorAgent(config.get('illustrator', {}))
    service = AgentService(agent, 'IllustratorService', port)
    service.start(background=False)


def run_publisher_service(port: int = 8003, config_path: str = None):
    """Run Publisher Agent as a service"""
    from agents.publisher_agent import PublisherAgent
    import yaml
    
    if config_path:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {}
    
    agent = PublisherAgent(config.get('publisher', {}))
    service = AgentService(agent, 'PublisherService', port)
    service.start(background=False)
