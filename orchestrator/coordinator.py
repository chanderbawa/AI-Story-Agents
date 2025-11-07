"""
Story Orchestrator - Coordinates all agents to create complete stories
"""

from typing import Dict, List, Any, Optional
import logging
from agents import AuthorAgent, IllustratorAgent, PublisherAgent, Message

logging.basicConfig(level=logging.INFO)


class StoryOrchestrator:
    """
    Orchestrates the multi-agent story creation process.
    
    Workflow:
    1. Receive story idea from user
    2. Coordinate Author to create story
    3. Coordinate Illustrator to create images
    4. Coordinate Publisher to assemble final product
    5. Handle agent communication and feedback loops
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.logger = logging.getLogger("Orchestrator")
        
        # Initialize agents
        self.logger.info("🎬 Initializing Story Creation Agents...")
        
        self.author = AuthorAgent(self.config.get('author', {}))
        self.illustrator = IllustratorAgent(self.config.get('illustrator', {}))
        self.publisher = PublisherAgent(self.config.get('publisher', {}))
        
        self.agents = {
            'AuthorAgent': self.author,
            'IllustratorAgent': self.illustrator,
            'PublisherAgent': self.publisher
        }
        
        # Message queue for agent communication
        self.message_queue: List[Message] = []
        
        self.logger.info("✅ All agents initialized and ready")
    
    def create_story(self, story_idea: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main workflow to create a complete story from an idea.
        
        Args:
            story_idea: Dictionary containing:
                - plot: Story plot/idea
                - target_age: Target age range
                - themes: List of themes
                - length: 'short', 'medium', or 'long'
                - art_style: Visual style preference
                
        Returns:
            Complete story with text, images, and publication files
        """
        
        self.logger.info("=" * 60)
        self.logger.info("🎬 STARTING STORY CREATION WORKFLOW")
        self.logger.info("=" * 60)
        self.logger.info(f"Plot: {story_idea.get('plot', 'No plot provided')}")
        self.logger.info(f"Target Age: {story_idea.get('target_age', '8-12')}")
        self.logger.info(f"Themes: {', '.join(story_idea.get('themes', []))}")
        self.logger.info("=" * 60)
        
        # Phase 1: Story Writing
        self.logger.info("\n📝 PHASE 1: STORY CREATION")
        self.logger.info("-" * 60)
        
        story_result = self._phase_story_creation(story_idea)
        
        if story_result['status'] != 'complete':
            return {'status': 'error', 'message': 'Story creation failed'}
        
        # Phase 2: Illustration
        self.logger.info("\n🎨 PHASE 2: ILLUSTRATION GENERATION")
        self.logger.info("-" * 60)
        
        illustration_result = self._phase_illustration(
            story_result,
            story_idea.get('art_style', 'children_book')
        )
        
        if illustration_result['status'] != 'complete':
            return {'status': 'error', 'message': 'Illustration failed'}
        
        # Phase 3: Publication
        self.logger.info("\n📚 PHASE 3: PUBLICATION ASSEMBLY")
        self.logger.info("-" * 60)
        
        publication_result = self._phase_publication(
            story_result,
            illustration_result,
            story_idea
        )
        
        self.logger.info("\n" + "=" * 60)
        self.logger.info("✅ STORY CREATION COMPLETE!")
        self.logger.info("=" * 60)
        
        return {
            'status': 'complete',
            'story': story_result['story'],
            'images': illustration_result['images'],
            'publications': publication_result['files'],
            'metadata': {
                'title': story_idea.get('plot', 'Untitled')[:50],
                'chapters': len(story_result['chapters']),
                'images': len(illustration_result['images']),
                'page_count': publication_result.get('page_count', 0)
            }
        }
    
    def _phase_story_creation(self, story_idea: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 1: Author creates the story."""
        
        # Send task to Author Agent
        message = Message(
            sender="Orchestrator",
            recipient="AuthorAgent",
            content={
                'action': 'create_story',
                'plot': story_idea.get('plot', ''),
                'themes': story_idea.get('themes', []),
                'target_age': story_idea.get('target_age', '8-12'),
                'length': story_idea.get('length', 'short')
            },
            message_type="request"
        )
        
        # Author processes the task
        response = self.author.receive_message(message)
        
        if response and response.content.get('status') == 'complete':
            self.logger.info(f"✅ Story created: {len(response.content['chapters'])} chapters")
            return response.content
        
        return {'status': 'error'}
    
    def _phase_illustration(self, story_result: Dict[str, Any], 
                           art_style: str) -> Dict[str, Any]:
        """Phase 2: Illustrator creates images."""
        
        # Prepare illustration request
        scenes = story_result.get('illustration_scenes', [])
        characters = story_result['story'].get('characters', [])
        
        self.logger.info(f"Generating {len(scenes)} illustrations...")
        
        # Check if scenes need clarification
        for scene in scenes:
            if self._scene_needs_clarification(scene):
                # Illustrator requests clarification from Author
                clarification_msg = Message(
                    sender="IllustratorAgent",
                    recipient="AuthorAgent",
                    content={
                        'action': 'describe_scene',
                        'scene_id': scene.get('id')
                    },
                    message_type="request"
                )
                
                author_response = self.author.receive_message(clarification_msg)
                
                if author_response:
                    # Update scene with enhanced description
                    scene['description'] = author_response.content.get('description', scene['description'])
        
        # Send illustration task
        message = Message(
            sender="Orchestrator",
            recipient="IllustratorAgent",
            content={
                'action': 'generate_illustrations',
                'scenes': scenes,
                'characters': characters,
                'art_style': art_style
            },
            message_type="request"
        )
        
        response = self.illustrator.receive_message(message)
        
        if response and response.content.get('status') == 'complete':
            self.logger.info(f"✅ Generated {len(response.content['images'])} illustrations")
            return response.content
        
        return {'status': 'error'}
    
    def _phase_publication(self, story_result: Dict[str, Any],
                          illustration_result: Dict[str, Any],
                          story_idea: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 3: Publisher assembles final product."""
        
        message = Message(
            sender="Orchestrator",
            recipient="PublisherAgent",
            content={
                'action': 'publish',
                'story': story_result['story'],
                'images': illustration_result['images'],
                'title': story_idea.get('plot', 'Untitled Story')[:50],
                'output_dir': self.config.get('output_dir', 'output/publications')
            },
            message_type="request"
        )
        
        response = self.publisher.receive_message(message)
        
        if response and response.content.get('status') == 'complete':
            files = response.content.get('files', {})
            self.logger.info(f"✅ Published in {len(files)} formats")
            for format_type, filepath in files.items():
                self.logger.info(f"   📄 {format_type.upper()}: {filepath}")
            return response.content
        
        return {'status': 'error'}
    
    def _scene_needs_clarification(self, scene: Dict) -> bool:
        """Determine if a scene description needs more detail."""
        
        description = scene.get('description', '')
        
        # Simple heuristic - in production, use AI
        if len(description) < 50:
            return True
        
        if not any(word in description.lower() for word in ['standing', 'sitting', 'looking']):
            return True
        
        return False
    
    def get_agent_status(self) -> Dict[str, str]:
        """Get current status of all agents."""
        
        return {
            name: agent.status
            for name, agent in self.agents.items()
        }
    
    def send_message_between_agents(self, sender_name: str, 
                                    recipient_name: str,
                                    content: Dict[str, Any],
                                    message_type: str = "info"):
        """Facilitate communication between agents."""
        
        if sender_name not in self.agents or recipient_name not in self.agents:
            self.logger.error(f"Invalid agent names: {sender_name} -> {recipient_name}")
            return
        
        sender = self.agents[sender_name]
        recipient = self.agents[recipient_name]
        
        message = sender.send_message(recipient_name, content, message_type)
        response = recipient.receive_message(message)
        
        if response:
            sender.receive_message(response)
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for all agents."""
        
        return {
            'author': {
                'model_name': 'mistralai/Mistral-7B-Instruct-v0.2',
                'device': 'auto',
                'load_in_8bit': True,
                'temperature': 0.7,
                'top_p': 0.9,
                'writing_style': 'engaging',
                'target_age': '8-12',
                'load_model': False  # Set to True when ready to use
            },
            'illustrator': {
                'model_name': 'runwayml/stable-diffusion-v1-5',
                'device': 'auto',
                'art_style': 'children_book',
                'num_inference_steps': 50,
                'guidance_scale': 7.5,
                'width': 768,
                'height': 1024,
                'negative_prompt': 'blurry, distorted, low quality, text, watermark',
                'load_model': False  # Set to True when ready to use
            },
            'publisher': {
                'formats': ['pdf', 'html'],
                'layout': {
                    'page_width': 6,
                    'page_height': 9
                }
            },
            'output_dir': 'output/publications'
        }
    
    def __repr__(self):
        return f"StoryOrchestrator(agents={len(self.agents)}, status={self.get_agent_status()})"
