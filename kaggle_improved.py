"""
Kaggle - IMPROVED VERSION for Kids' Stories
Better model + Better prompts = Better results
"""

import torch
import os
import sys
import importlib.util

print("="*70)
print("🎨 KIDS' STORY GENERATOR - IMPROVED")
print("="*70)
print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
print("="*70)

torch.cuda.empty_cache()

# Setup
print("\n📥 Setting up...")
os.chdir('/kaggle/working')
if not os.path.exists('AI-Story-Agents'):
    get_ipython().system('git clone https://github.com/chanderbawa/AI-Story-Agents.git')
os.chdir('/kaggle/working/AI-Story-Agents')

# Install
print("\n📦 Installing...")
get_ipython().system('pip install -q -r requirements.txt')

# Configure with BETTER model
print("\n⚙️  Configuring for QUALITY kids' stories...")
import yaml

with open('config/agents_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Use Phi-2 - much better than TinyLlama for creative writing
config['author']['device'] = 'cuda'
config['author']['load_in_8bit'] = False
config['author']['model_name'] = 'microsoft/phi-2'  # Better model!
config['author']['max_length'] = 400
config['author']['temperature'] = 0.8  # More creative
config['author']['top_p'] = 0.9

# Better image generation for kids' books
config['illustrator']['device'] = 'cuda'
config['illustrator']['model_name'] = 'runwayml/stable-diffusion-v1-5'
config['illustrator']['width'] = 768  # Higher quality
config['illustrator']['height'] = 768
config['illustrator']['num_inference_steps'] = 25  # Better quality
config['illustrator']['guidance_scale'] = 8.0  # Stronger prompt following

with open('config/agents_config.yaml', 'w') as f:
    yaml.dump(config, f)

print("✅ Using Phi-2 (2.7B) - Much better for stories!")
print("✅ Image size: 768x768 with 25 steps")

# Direct import
spec = importlib.util.spec_from_file_location(
    "coordinator", 
    "/kaggle/working/AI-Story-Agents/orchestrator/coordinator.py"
)
coordinator_module = importlib.util.module_from_spec(spec)
sys.modules['coordinator'] = coordinator_module
spec.loader.exec_module(coordinator_module)

StoryOrchestrator = coordinator_module.StoryOrchestrator

# Initialize
print("\n📥 Loading models (3-4 min)...")
print("   Phi-2: ~5 GB")
print("   Stable Diffusion: ~4 GB")

orchestrator = StoryOrchestrator(config)

print(f"✅ Loaded! GPU: {torch.cuda.memory_allocated()/1e9:.2f} GB / {torch.cuda.get_device_properties(0).total_memory/1e9:.2f} GB")

# BETTER story prompt for kids
story_idea = {
    'plot': '''
    Leo is a friendly 9-year-old boy who loves making friends.
    
    On his first day at Sunshine Elementary School, Leo feels nervous.
    During recess, he sees a boy named Finn sitting alone on the Friendship Bench.
    Finn looks sad because he's new and doesn't have any friends yet.
    
    Leo walks over with a big smile and says "Hi! Want to play together?"
    Finn's face lights up with happiness.
    
    They play tag, share snacks, and laugh together.
    By the end of recess, they are best friends.
    Leo learns that being kind and brave helps make wonderful friendships.
    ''',
    'target_age': '6-8',  # Younger for simpler language
    'themes': ['friendship', 'kindness', 'bravery'],
    'length': 'short',
    'art_style': 'cartoon'  # Cartoon style for kids!
}

print("\n📖 CREATING KIDS' STORY")
print("="*70)
print(f"Title: Leo's First Day")
print(f"Style: Cartoon illustrations for children")
print(f"⏱️  Estimated: 6-8 minutes")
print("="*70)

# Generate
import time
start = time.time()

result = orchestrator.create_story(story_idea)

elapsed = time.time() - start

# Results
print("\n" + "="*70)
if result['status'] == 'complete':
    print(f"✅ COMPLETE in {elapsed/60:.1f} minutes!")
    print("="*70)
    
    print(f"\n📊 {result['metadata']['chapters']} chapters, {result['metadata']['images']} images")
    
    # Save files
    import shutil
    import zipfile
    
    pdf_dest = '/kaggle/working/leos_story.pdf'
    html_dest = '/kaggle/working/leos_story.html'
    zip_path = '/kaggle/working/leos_story.zip'
    
    shutil.copy2(result['publications']['pdf'], pdf_dest)
    shutil.copy2(result['publications']['html'], html_dest)
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(pdf_dest, 'leos_story.pdf')
        zipf.write(html_dest, 'leos_story.html')
    
    print(f"\n📦 leos_story.zip ({os.path.getsize(zip_path)/1024/1024:.1f} MB)")
    
    # Download
    from IPython.display import FileLink, display
    
    print("\n📥 DOWNLOAD YOUR KIDS' BOOK:")
    print("="*70)
    display(FileLink(zip_path))
    display(FileLink(pdf_dest))
    display(FileLink(html_dest))
    
    print("\n🎉 Kids' story book complete!")
    print("   - Cartoon-style illustrations")
    print("   - Age-appropriate language")
    print("   - Positive message about friendship")
    
else:
    print(f"❌ Failed: {result.get('message')}")

print("\n✨ DONE!")
