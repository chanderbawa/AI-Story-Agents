"""
Kaggle - Using Flan-T5 for Better Story Generation
Flan-T5 is instruction-tuned and much better at following prompts than TinyLlama
"""

import os
import sys

print("="*70)
print("📖 AI STORY GENERATOR - BETTER MODEL")
print("="*70)

# Setup
os.chdir('/kaggle/working')
if not os.path.exists('AI-Story-Agents'):
    get_ipython().system('git clone https://github.com/chanderbawa/AI-Story-Agents.git')
os.chdir('/kaggle/working/AI-Story-Agents')

get_ipython().system('pip install -q -r requirements.txt')

# ============================================
# STEP 1: Use Flan-T5 (instruction-tuned model)
# ============================================

print("\n⚙️  Configuring with Flan-T5 (better at following instructions)")

import yaml

with open('config/agents_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Use Flan-T5-Large - instruction-tuned, better than TinyLlama
config['author']['device'] = 'cuda'  # GPU for faster generation
config['author']['model_name'] = 'google/flan-t5-large'  # 780M params, instruction-tuned!
config['author']['load_in_8bit'] = False
config['author']['max_length'] = 512
config['author']['temperature'] = 0.8
config['author']['top_p'] = 0.95

# Illustrator settings
config['illustrator']['device'] = 'cuda'
config['illustrator']['width'] = 512
config['illustrator']['height'] = 512
config['illustrator']['num_inference_steps'] = 20

with open('config/agents_config.yaml', 'w') as f:
    yaml.dump(config, f)

print("✅ Using Flan-T5-Large (instruction-tuned for better results)")

# ============================================
# STEP 2: Patch Author Agent to use Flan-T5
# ============================================

print("\n🔧 Patching Author Agent for Flan-T5...")

# Flan-T5 uses seq2seq, not causal LM
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch

class FlanT5AuthorAgent:
    """Author agent using Flan-T5 for better instruction following."""
    
    def __init__(self, config):
        self.config = config
        self.model_name = config.get('model_name', 'google/flan-t5-large')
        self.device = config.get('device', 'cuda')
        
        print(f"Loading {self.model_name}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.model_name,
            device_map=self.device
        )
        
        print("✅ Model loaded")
    
    def generate_text(self, prompt, max_length=512):
        """Generate text using Flan-T5."""
        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        
        if self.device == 'cuda':
            inputs = {k: v.to('cuda') for k, v in inputs.items()}
        
        outputs = self.model.generate(
            **inputs,
            max_length=max_length,
            temperature=self.config.get('temperature', 0.8),
            top_p=self.config.get('top_p', 0.95),
            do_sample=True,
            num_return_sequences=1
        )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    def create_story(self, story_idea):
        """Create a complete story from plot."""
        plot = story_idea['plot']
        target_age = story_idea.get('target_age', '6-8')
        themes = ', '.join(story_idea.get('themes', ['friendship']))
        
        print("\n📝 Generating story chapters...")
        
        chapters = []
        
        # Generate 3 chapters
        for i in range(1, 4):
            print(f"\n✍️  Writing Chapter {i}...")
            
            # Better prompt for Flan-T5
            prompt = f"""Write Chapter {i} of a children's story for ages {target_age}.

Story Plot: {plot}

Themes: {themes}

Instructions:
- Write in simple, clear language for young readers
- Include dialogue between characters
- Describe what characters see, hear, and feel
- Make it engaging and fun
- Length: 150-200 words

Chapter {i}:"""

            chapter_text = self.generate_text(prompt, max_length=300)
            
            chapters.append({
                'number': i,
                'title': f'Chapter {i}',
                'text': chapter_text
            })
            
            print(f"✅ Chapter {i} complete ({len(chapter_text)} chars)")
        
        return {
            'chapters': chapters,
            'plot': plot,
            'themes': story_idea.get('themes', []),
            'target_age': target_age
        }

# Initialize
author = FlanT5AuthorAgent(config['author'])

# ============================================
# STEP 3: Generate Story
# ============================================

print("\n" + "="*70)
print("📖 GENERATING STORY")
print("="*70)

story_idea = {
    'plot': '''
    Leo is a 9-year-old boy starting at a new school called Sunshine Elementary.
    
    On his first day, he feels nervous walking into the classroom. His teacher Ms. Johnson welcomes him warmly.
    
    At recess, Leo sees a boy named Finn sitting alone on a yellow bench called the Friendship Bench. Finn looks sad.
    
    Leo walks over and says "Hi! I'm Leo. Want to play?" Finn smiles and says "Yes! I'm Finn!"
    
    They play tag together and laugh. They share snacks under a tree.
    
    By the end of recess, they are best friends. Leo learns that being kind and brave helps make wonderful friendships.
    ''',
    'target_age': '6-8',
    'themes': ['friendship', 'kindness', 'bravery'],
    'length': 'short'
}

story_data = author.create_story(story_idea)

# Display
print("\n" + "="*70)
print("📚 STORY GENERATED")
print("="*70)

for chapter in story_data['chapters']:
    print(f"\n{'='*70}")
    print(f"CHAPTER {chapter['number']}")
    print(f"{'='*70}")
    print(chapter['text'])
    print()

# Save
import pickle
with open('/kaggle/working/story_data.pkl', 'wb') as f:
    pickle.dump(story_data, f)

print("\n" + "="*70)
print("🛑 REVIEW THE STORY")
print("="*70)
print("✅ If good → Continue to Cell 2 for illustrations")
print("❌ If bad → Adjust prompt and re-run")
