"""
Illustrator Agent - Visual Artist
Generates illustrations that support the story narrative.
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, Message
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import torch
from PIL import Image


class IllustratorAgent(BaseAgent):
    """
    AI agent specialized in creating story illustrations.
    
    Capabilities:
    - Scene interpretation and visualization
    - Character consistency across images
    - Art style adaptation
    - Visual storytelling
    - Feedback to author about visual clarity
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            name="IllustratorAgent",
            role="Visual Artist & Illustrator",
            config=config
        )
        
        self.art_style = config.get('art_style', 'children book illustration')
        self.pipeline = None
        
        # Visual memory for consistency
        self.character_references = {}
        self.generated_images = []
        self.style_prompts = {
            'children_book': 'children book illustration, colorful, friendly, hand-drawn style',
            'cartoon': 'cartoon style, expressive, bold lines, vibrant colors',
            'watercolor': 'watercolor illustration, soft colors, artistic, gentle',
            'line_art': 'black and white line art, detailed, expressive, high contrast'
        }
        
        if config.get('load_model', True):
            self._load_model()
    
    def _load_model(self):
        """Load the image generation model."""
        self.update_status("loading", "Loading image generation model...")
        
        model_name = self.config.get('model_name', 'runwayml/stable-diffusion-v1-5')
        device = self.config.get('device', 'cuda' if torch.cuda.is_available() else 'cpu')
        
        self.logger.info(f"Loading model: {model_name}")
        
        self.pipeline = StableDiffusionPipeline.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if device == 'cuda' else torch.float32,
            safety_checker=None
        )
        
        if device == 'cuda':
            self.pipeline = self.pipeline.to(device)
        
        # Optimize for speed
        self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipeline.scheduler.config
        )
        
        self.update_status("ready", "Model loaded successfully")
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process messages from other agents."""
        
        if message.message_type == "request":
            if message.content.get('action') == 'generate_illustrations':
                # Orchestrator requesting illustrations
                result = self.execute_task(message.content)
                return self.send_message(
                    message.sender,
                    result,
                    "response"
                )
            
            elif message.content.get('action') == 'create_character_reference':
                # Create consistent character reference
                char_data = message.content.get('character')
                reference = self._create_character_reference(char_data)
                return self.send_message(
                    message.sender,
                    {'character': char_data['name'], 'reference': reference},
                    "response"
                )
            
            elif message.content.get('action') == 'clarify_scene':
                # Request clarification from author
                scene_id = message.content.get('scene_id')
                return self.send_message(
                    "AuthorAgent",
                    {'action': 'describe_scene', 'scene_id': scene_id},
                    "request"
                )
        
        elif message.message_type == "response":
            # Received clarification from author
            if 'scene_id' in message.content and 'description' in message.content:
                # Use enhanced description to generate image
                pass
        
        return None
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main task execution for illustration generation.
        
        Args:
            task: Contains scenes, characters, art_style, etc.
            
        Returns:
            Generated images with metadata
        """
        self.update_status("working", "Creating illustrations...")
        
        scenes = task.get('scenes', [])
        characters = task.get('characters', [])
        art_style = task.get('art_style', self.art_style)
        
        # Step 1: Create character references
        self.logger.info("🎨 Creating character references...")
        for character in characters:
            self._create_character_reference(character)
        
        # Step 2: Generate scene illustrations
        self.logger.info(f"🎨 Generating {len(scenes)} illustrations...")
        generated_images = []
        
        for i, scene in enumerate(scenes):
            self.logger.info(f"Generating image {i+1}/{len(scenes)}: {scene.get('description', '')[:50]}...")
            
            image_data = self._generate_scene_image(scene, art_style)
            generated_images.append(image_data)
        
        self.generated_images.extend(generated_images)
        
        self.update_status("ready", f"Generated {len(generated_images)} illustrations")
        
        return {
            'images': generated_images,
            'character_references': self.character_references,
            'status': 'complete'
        }
    
    def _create_character_reference(self, character: Dict) -> Dict:
        """Create a visual reference for character consistency."""
        
        name = character.get('name', 'Character')
        
        if name in self.character_references:
            self.logger.info(f"Character reference for {name} already exists")
            return self.character_references[name]
        
        self.logger.info(f"Creating character reference for {name}")
        
        # Build character description prompt
        physical = character.get('physical', '')
        age = character.get('age', 10)
        personality = character.get('personality', '')
        
        prompt = f"""Character reference sheet, {name}, age {age}, {physical}, 
{personality} personality, {self.art_style}, character design, 
full body, front view, clean background, high quality"""
        
        negative_prompt = self.config.get('negative_prompt', 
            'blurry, distorted, low quality, text, watermark')
        
        # Generate reference image
        if self.pipeline:
            image = self.pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=self.config.get('num_inference_steps', 30),
                guidance_scale=self.config.get('guidance_scale', 7.5),
                width=512,
                height=512
            ).images[0]
        else:
            # Placeholder if model not loaded
            image = Image.new('RGB', (512, 512), color='lightgray')
        
        reference = {
            'name': name,
            'image': image,
            'prompt': prompt,
            'description': f"{physical}, {personality}"
        }
        
        self.character_references[name] = reference
        
        return reference
    
    def _generate_scene_image(self, scene: Dict, art_style: str) -> Dict:
        """Generate an illustration for a specific scene."""
        
        scene_id = scene.get('id', 'unknown')
        description = scene.get('description', '')
        characters = scene.get('characters', [])
        mood = scene.get('mood', 'neutral')
        
        # Build comprehensive prompt
        character_desc = self._get_character_descriptions(characters)
        style_prompt = self.style_prompts.get(art_style.replace(' ', '_'), art_style)
        
        prompt = f"""{description}, {character_desc}, {mood} mood, 
{style_prompt}, high quality, detailed, professional illustration"""
        
        negative_prompt = self.config.get('negative_prompt',
            'blurry, distorted, low quality, text, watermark, multiple limbs')
        
        # Generate image
        if self.pipeline:
            image = self.pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=self.config.get('num_inference_steps', 50),
                guidance_scale=self.config.get('guidance_scale', 7.5),
                width=self.config.get('width', 768),
                height=self.config.get('height', 1024)
            ).images[0]
        else:
            # Placeholder
            image = Image.new('RGB', (768, 1024), color='lightblue')
        
        image_data = {
            'scene_id': scene_id,
            'image': image,
            'prompt': prompt,
            'chapter': scene.get('chapter', 1),
            'description': description,
            'characters': characters
        }
        
        return image_data
    
    def _get_character_descriptions(self, character_names: List[str]) -> str:
        """Get visual descriptions of characters for prompt."""
        
        descriptions = []
        for name in character_names:
            if name in self.character_references:
                ref = self.character_references[name]
                descriptions.append(ref['description'])
        
        return ', '.join(descriptions) if descriptions else ''
    
    def save_images(self, output_dir: str):
        """Save all generated images to directory."""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for img_data in self.generated_images:
            scene_id = img_data['scene_id']
            filename = f"{output_dir}/{scene_id}.png"
            img_data['image'].save(filename)
            self.logger.info(f"Saved: {filename}")
    
    def provide_feedback_to_author(self, scene: Dict) -> Dict:
        """Provide feedback about visual clarity of scene description."""
        
        feedback = {
            'scene_id': scene.get('id'),
            'clarity': 'good',  # Could use AI to assess
            'suggestions': [],
            'missing_details': []
        }
        
        # Check for essential visual elements
        description = scene.get('description', '')
        
        if not any(word in description.lower() for word in ['standing', 'sitting', 'walking']):
            feedback['missing_details'].append('character positions')
        
        if not any(word in description.lower() for word in ['room', 'outside', 'garden', 'school']):
            feedback['missing_details'].append('setting details')
        
        if feedback['missing_details']:
            feedback['clarity'] = 'needs_improvement'
            feedback['suggestions'].append(
                f"Please clarify: {', '.join(feedback['missing_details'])}"
            )
        
        return feedback
    
    def get_capabilities(self) -> List[str]:
        """Return list of illustrator capabilities."""
        return [
            'scene_illustration',
            'character_design',
            'style_adaptation',
            'visual_consistency',
            'mood_expression',
            'composition'
        ]
