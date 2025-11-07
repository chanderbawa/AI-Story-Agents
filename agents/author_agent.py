"""
Author Agent - Middle School Story Writer
Generates creative, age-appropriate stories from plot ideas.
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, Message
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch


class AuthorAgent(BaseAgent):
    """
    AI agent specialized in writing middle-grade stories.
    
    Capabilities:
    - Plot development from simple ideas
    - Character creation and development
    - Dialogue writing
    - Scene description for illustrators
    - Story pacing and structure
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            name="AuthorAgent",
            role="Middle School Story Writer",
            config=config
        )
        
        self.writing_style = config.get('writing_style', 'engaging')
        self.target_age = config.get('target_age', '8-12')
        self.model = None
        self.tokenizer = None
        self.generator = None  # Initialize generator attribute
        
        # Story state
        self.current_story = {
            'plot': None,
            'characters': [],
            'chapters': [],
            'themes': [],
            'scenes_for_illustration': []
        }
        
        if config.get('load_model', True):
            self._load_model()
    
    def _load_model(self):
        """Load the language model for story generation."""
        try:
            self.update_status("loading", "Loading language model...")
            
            model_name = self.config.get('model_name', 'mistralai/Mistral-7B-Instruct-v0.2')
            device = self.config.get('device', 'auto')
            load_in_8bit = self.config.get('load_in_8bit', False)
            
            self.logger.info(f"Loading model: {model_name}")
            self.logger.info(f"Device: {device}, 8-bit: {load_in_8bit}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            load_kwargs = {'device_map': device}
            if load_in_8bit and torch.cuda.is_available():
                load_kwargs['load_in_8bit'] = True
            elif load_in_8bit and not torch.cuda.is_available():
                self.logger.warning("8-bit loading requested but CUDA not available. Loading in full precision.")
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                **load_kwargs
            )
            
            # Create text generation pipeline
            self.generator = pipeline(
                'text-generation',
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=1024,
                do_sample=True,
                temperature=self.config.get('temperature', 0.7),
                top_p=self.config.get('top_p', 0.9)
            )
            
            self.logger.info("✅ Model loaded successfully")
            self.update_status("ready", "Model loaded successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load model: {str(e)}")
            self.generator = None
            raise RuntimeError(f"Failed to load Author model: {str(e)}")
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process messages from other agents."""
        
        if message.message_type == "request":
            if message.content.get('action') == 'create_story':
                # Orchestrator requesting story creation
                result = self.execute_task(message.content)
                return self.send_message(
                    message.sender,
                    result,
                    "response"
                )
            
            elif message.content.get('action') == 'describe_scene':
                # Illustrator requesting scene details
                scene_id = message.content.get('scene_id')
                description = self._enhance_scene_description(scene_id)
                return self.send_message(
                    message.sender,
                    {'scene_id': scene_id, 'description': description},
                    "response"
                )
        
        return None
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main task execution for story creation.
        
        Args:
            task: Contains plot, themes, target_age, length, etc.
            
        Returns:
            Complete story with chapters and illustration notes
        """
        self.update_status("working", "Creating story...")
        
        # Extract task parameters
        plot_idea = task.get('plot', '')
        themes = task.get('themes', [])
        length = task.get('length', 'short')
        
        # Store story context
        self.current_story['plot'] = plot_idea
        self.current_story['themes'] = themes
        
        # Step 1: Develop characters
        self.logger.info("📝 Developing characters...")
        characters = self._develop_characters(plot_idea, themes)
        self.current_story['characters'] = characters
        
        # Step 2: Create story outline
        self.logger.info("📝 Creating story outline...")
        outline = self._create_outline(plot_idea, characters, length)
        
        # Step 3: Write chapters
        self.logger.info("📝 Writing chapters...")
        chapters = []
        for i, chapter_outline in enumerate(outline):
            chapter = self._write_chapter(i + 1, chapter_outline, characters)
            chapters.append(chapter)
            
            # Identify scenes for illustration
            scenes = self._identify_illustration_scenes(chapter)
            self.current_story['scenes_for_illustration'].extend(scenes)
        
        self.current_story['chapters'] = chapters
        
        self.update_status("ready", f"Story complete: {len(chapters)} chapters")
        
        return {
            'story': self.current_story,
            'status': 'complete',
            'chapters': chapters,
            'illustration_scenes': self.current_story['scenes_for_illustration']
        }
    
    def _develop_characters(self, plot: str, themes: List[str]) -> List[Dict]:
        """Develop main characters based on plot and themes."""
        
        prompt = f"""Create 2-3 main characters for a middle-grade story.

Plot: {plot}
Themes: {', '.join(themes)}
Target Age: {self.target_age}

For each character, provide:
- Name
- Age
- Physical description
- Personality traits
- Role in the story

Format as a character list."""

        response = self._generate_text(prompt, max_length=500)
        
        # Parse response into character objects
        # (In production, use structured output or JSON)
        characters = self._parse_characters(response)
        
        return characters
    
    def _create_outline(self, plot: str, characters: List[Dict], 
                       length: str) -> List[Dict]:
        """Create chapter-by-chapter outline."""
        
        num_chapters = {'short': 3, 'medium': 5, 'long': 8}.get(length, 3)
        
        char_names = [c['name'] for c in characters]
        
        prompt = f"""Create a {num_chapters}-chapter outline for a middle-grade story.

Plot: {plot}
Characters: {', '.join(char_names)}
Target Age: {self.target_age}

For each chapter, provide:
1. Chapter title
2. Key events
3. Character development
4. Emotional arc

Format as a numbered list."""

        response = self._generate_text(prompt, max_length=800)
        
        # Parse into chapter outlines
        outlines = self._parse_outline(response, num_chapters)
        
        return outlines
    
    def _write_chapter(self, chapter_num: int, outline: Dict, 
                      characters: List[Dict]) -> Dict:
        """Write a complete chapter based on outline."""
        
        self.logger.info(f"Writing Chapter {chapter_num}: {outline.get('title', '')}")
        
        char_descriptions = "\n".join([
            f"- {c['name']}: {c.get('personality', '')}"
            for c in characters
        ])
        
        prompt = f"""Write Chapter {chapter_num} of a middle-grade story.

Chapter Title: {outline.get('title', f'Chapter {chapter_num}')}
Chapter Outline: {outline.get('events', '')}

Characters:
{char_descriptions}

Writing Style: {self.writing_style}
Target Age: {self.target_age}

Write an engaging, age-appropriate chapter with dialogue, action, and emotion.
Length: 800-1200 words."""

        chapter_text = self._generate_text(prompt, max_length=1500)
        
        return {
            'number': chapter_num,
            'title': outline.get('title', f'Chapter {chapter_num}'),
            'text': chapter_text,
            'outline': outline
        }
    
    def _identify_illustration_scenes(self, chapter: Dict) -> List[Dict]:
        """Identify 2-3 key scenes in chapter that need illustration."""
        
        # Use AI to identify visual moments
        prompt = f"""Identify 2-3 key visual scenes from this chapter that would make great illustrations.

Chapter: {chapter['title']}
Text: {chapter['text'][:500]}...

For each scene, provide:
- Scene description
- Characters present
- Mood/emotion
- Visual focus

Format as a list."""

        response = self._generate_text(prompt, max_length=400)
        
        scenes = self._parse_scenes(response, chapter['number'])
        
        return scenes
    
    def _enhance_scene_description(self, scene_id: str) -> str:
        """Provide detailed description for illustrator."""
        
        # Find scene in current story
        for scene in self.current_story['scenes_for_illustration']:
            if scene.get('id') == scene_id:
                prompt = f"""Provide detailed visual description for an illustrator.

Scene: {scene.get('description', '')}
Characters: {scene.get('characters', '')}
Mood: {scene.get('mood', '')}

Describe:
- Character positions and expressions
- Setting details
- Lighting and atmosphere
- Key visual elements

Be specific and visual."""

                enhanced = self._generate_text(prompt, max_length=300)
                return enhanced
        
        return "Scene not found"
    
    def _generate_text(self, prompt: str, max_length: int = 1000) -> str:
        """Generate text using the language model."""
        
        if not self.generator:
            return "[Model not loaded]"
        
        result = self.generator(
            prompt,
            max_new_tokens=max_length,
            temperature=self.config.get('temperature', 0.7),
            top_p=self.config.get('top_p', 0.9),
            do_sample=True
        )
        
        return result[0]['generated_text'].replace(prompt, '').strip()
    
    def _parse_characters(self, text: str) -> List[Dict]:
        """Parse character descriptions from generated text."""
        # Simplified parsing - in production, use structured output
        return [
            {'name': 'Character1', 'age': 10, 'personality': 'brave'},
            {'name': 'Character2', 'age': 9, 'personality': 'clever'}
        ]
    
    def _parse_outline(self, text: str, num_chapters: int) -> List[Dict]:
        """Parse chapter outline from generated text."""
        # Simplified - in production, use structured parsing
        return [
            {'title': f'Chapter {i+1}', 'events': 'Key events...'}
            for i in range(num_chapters)
        ]
    
    def _parse_scenes(self, text: str, chapter_num: int) -> List[Dict]:
        """Parse scene descriptions from generated text."""
        # Simplified - in production, use structured parsing
        return [
            {
                'id': f'ch{chapter_num}_scene{i+1}',
                'chapter': chapter_num,
                'description': 'Scene description...',
                'characters': [],
                'mood': 'exciting'
            }
            for i in range(2)
        ]
    
    def get_capabilities(self) -> List[str]:
        """Return list of author capabilities."""
        return [
            'plot_development',
            'character_creation',
            'dialogue_writing',
            'scene_description',
            'story_pacing',
            'theme_integration'
        ]
