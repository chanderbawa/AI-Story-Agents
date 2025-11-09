"""
Kaggle TPU - Step-by-Step Story Generation
Review each agent's output before proceeding
"""

import os
import sys

print("="*70)
print("🚀 TPU-POWERED KIDS' STORY GENERATOR")
print("="*70)

# Check TPU availability
try:
    import torch_xla
    import torch_xla.core.xla_model as xm
    device = xm.xla_device()
    print(f"✅ TPU Available: {device}")
except:
    print("⚠️  TPU not available, using GPU/CPU")
    import torch
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"   Using: {device}")

print("="*70)

# Setup
print("\n📥 Setting up...")
os.chdir('/kaggle/working')
if not os.path.exists('AI-Story-Agents'):
    get_ipython().system('git clone https://github.com/chanderbawa/AI-Story-Agents.git')
os.chdir('/kaggle/working/AI-Story-Agents')

get_ipython().system('pip install -q -r requirements.txt')

# For TPU support
get_ipython().system('pip install -q torch-xla cloud-tpu-client')

print("✅ Setup complete")

# ============================================
# STEP 1: CONFIGURE
# ============================================

print("\n" + "="*70)
print("STEP 1: CONFIGURATION")
print("="*70)

import yaml

with open('config/agents_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Use smaller, better models
config['author']['device'] = 'cpu'  # Text on CPU (TPU doesn't help much for autoregressive text)
config['author']['model_name'] = 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'
config['author']['max_length'] = 500
config['author']['temperature'] = 0.7
config['author']['top_p'] = 0.9

# Images can use GPU/TPU
config['illustrator']['device'] = str(device) if 'xla' not in str(device) else 'cpu'
config['illustrator']['width'] = 512
config['illustrator']['height'] = 512
config['illustrator']['num_inference_steps'] = 20

with open('config/agents_config.yaml', 'w') as f:
    yaml.dump(config, f)

print("✅ Configuration saved")
print(f"   Author: CPU (text generation)")
print(f"   Illustrator: {config['illustrator']['device']}")

# ============================================
# STEP 2: LOAD AUTHOR AGENT ONLY
# ============================================

print("\n" + "="*70)
print("STEP 2: LOADING AUTHOR AGENT")
print("="*70)

from agents.author_agent import AuthorAgent

author = AuthorAgent(config.get('author', {}))
print("✅ Author Agent loaded")

# ============================================
# STEP 3: GENERATE STORY TEXT
# ============================================

print("\n" + "="*70)
print("STEP 3: GENERATING STORY TEXT")
print("="*70)

# Your story idea
story_idea = {
    'plot': '''
    Leo is a cheerful 9-year-old boy with curly brown hair and a bright smile.
    
    It's his first day at Sunshine Elementary School. He feels nervous but excited.
    
    At recess, Leo sees a boy named Finn sitting alone on a yellow bench.
    Finn has red hair and looks sad because he's new and has no friends.
    
    Leo takes a deep breath, walks over, and says "Hi! I'm Leo. Want to play tag with me?"
    
    Finn's face lights up with a huge smile. "Yes! I'd love to!" he says.
    
    They run around the playground, laughing and playing.
    They share Leo's cookies during snack time.
    
    By the end of recess, they are best friends.
    
    Leo learns that being brave and kind helps you make wonderful friends.
    ''',
    'target_age': '6-8',
    'themes': ['friendship', 'kindness', 'bravery'],
    'length': 'short'
}

print(f"📖 Plot: {story_idea['plot'][:100]}...")
print(f"🎯 Target Age: {story_idea['target_age']}")
print(f"💭 Themes: {', '.join(story_idea['themes'])}")

# Create story request
from agents.base_agent import Message

request = Message(
    sender='User',
    recipient='AuthorAgent',
    message_type='request',
    content={
        'action': 'create_story',
        'story_idea': story_idea
    }
)

print("\n⏳ Generating story text (this may take 2-3 minutes)...")
response = author.process_message(request)

# Display results
print("\n" + "="*70)
print("📝 STORY TEXT GENERATED")
print("="*70)

if response and response.content.get('status') == 'complete':
    story_data = response.content.get('story', {})
    chapters = story_data.get('chapters', [])
    
    print(f"✅ Generated {len(chapters)} chapters")
    
    # Show each chapter
    for i, chapter in enumerate(chapters, 1):
        print(f"\n{'='*70}")
        print(f"CHAPTER {i}: {chapter.get('title', f'Chapter {i}')}")
        print(f"{'='*70}")
        print(chapter.get('text', ''))
        print()
    
    # Ask for approval
    print("\n" + "="*70)
    print("⚠️  REVIEW THE STORY ABOVE")
    print("="*70)
    print("Does the story look good?")
    print("- If YES: Continue to next cell to generate illustrations")
    print("- If NO: Stop here and regenerate with different settings")
    print("="*70)
    
    # Save story data for next step
    import pickle
    with open('/kaggle/working/story_data.pkl', 'wb') as f:
        pickle.dump(story_data, f)
    
    print("\n✅ Story saved to story_data.pkl")
    
else:
    print("❌ Story generation failed!")
    print(f"Status: {response.content.get('status') if response else 'No response'}")
    print(f"Message: {response.content.get('message') if response else 'Unknown error'}")

print("\n" + "="*70)
print("🛑 STOP HERE - REVIEW THE STORY")
print("="*70)
print("If story looks good, run the NEXT cell to generate illustrations")
