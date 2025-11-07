"""
Kaggle Notebook - Distributed AI Story Agents
Copy this entire file into a Kaggle notebook cell and run!

SETUP:
1. Enable GPU: Right sidebar → Accelerator → GPU T4 x2
2. Copy this entire code
3. Paste into a Kaggle cell
4. Run!
"""

# ============================================
# STEP 1: GPU CHECK
# ============================================

import torch
print("="*70)
print("🔍 GPU CHECK")
print("="*70)

if torch.cuda.is_available():
    print(f"✅ GPU Available!")
    print(f"   GPU: {torch.cuda.get_device_name(0)}")
    print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
else:
    print("⚠️  GPU NOT Available - will use CPU (slower)")
    print("   To enable GPU: Right sidebar → Accelerator → GPU T4 x2")
    
print("="*70)

# ============================================
# STEP 2: INSTALL DEPENDENCIES
# ============================================

print("\n📦 Installing dependencies...")
get_ipython().system('pip install -q transformers diffusers accelerate torch torchvision pillow pyyaml reportlab flask')

# ============================================
# STEP 3: DOWNLOAD CODE
# ============================================

print("\n📥 Downloading AI Story Agents code...")

import os
import urllib.request

# Create directory structure
for dir_path in ['agents', 'orchestrator', 'config', 'distributed', 'output/publications']:
    os.makedirs(dir_path, exist_ok=True)

# Files to download
files = {
    'agents/__init__.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/agents/__init__.py',
    'agents/base_agent.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/agents/base_agent.py',
    'agents/author_agent.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/agents/author_agent.py',
    'agents/illustrator_agent.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/agents/illustrator_agent.py',
    'agents/publisher_agent.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/agents/publisher_agent.py',
    'orchestrator/__init__.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/orchestrator/__init__.py',
    'orchestrator/coordinator.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/orchestrator/coordinator.py',
    'config/agents_config.yaml': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/config/agents_config.yaml',
    'distributed/__init__.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/distributed/__init__.py',
    'distributed/message_broker.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/distributed/message_broker.py',
    'distributed/agent_service.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/distributed/agent_service.py',
    'distributed/distributed_orchestrator.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/distributed/distributed_orchestrator.py',
}

download_success = True
for filepath, url in files.items():
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"✅ {filepath}")
    except Exception as e:
        print(f"❌ {filepath}: {str(e)}")
        download_success = False

if not download_success:
    print("\n⚠️  Some files failed to download. Trying alternative method...")
    # Alternative: download as zip
    get_ipython().system('wget -q https://github.com/chanderbawa/AI-Story-Agents/archive/refs/heads/main.zip -O repo.zip')
    get_ipython().system('unzip -q repo.zip')
    get_ipython().system('cp -r AI-Story-Agents-main/* .')

print("\n✅ Code download complete!")

# ============================================
# STEP 4: START DISTRIBUTED SERVICES
# ============================================

print("\n🚀 Starting distributed agent services...")

import threading
import time
import logging
import yaml
from distributed.message_broker import get_broker
from distributed.agent_service import AgentService
from distributed.distributed_orchestrator import DistributedOrchestrator
from agents.author_agent import AuthorAgent
from agents.illustrator_agent import IllustratorAgent
from agents.publisher_agent import PublisherAgent

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(message)s'
)

# Load configuration
with open('config/agents_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize in-memory message broker
broker = get_broker(broker_type='memory')

# Start Author Service
print("📝 Starting Author Service...")
author_agent = AuthorAgent(config['author'])
author_service = AgentService(author_agent, 'AuthorService', 8001, broker)
author_service.start(background=True)
time.sleep(2)

# Start Illustrator Service
print("🎨 Starting Illustrator Service...")
illustrator_agent = IllustratorAgent(config['illustrator'])
illustrator_service = AgentService(illustrator_agent, 'IllustratorService', 8002, broker)
illustrator_service.start(background=True)
time.sleep(2)

# Start Publisher Service
print("📚 Starting Publisher Service...")
publisher_agent = PublisherAgent(config['publisher'])
publisher_service = AgentService(publisher_agent, 'PublisherService', 8003, broker)
publisher_service.start(background=True)
time.sleep(2)

print("\n✅ All distributed services are running!")
print("="*70)

# ============================================
# STEP 5: CREATE YOUR STORY
# ============================================

print("\n📖 STORY CONFIGURATION")
print("="*70)

# ⭐ CUSTOMIZE YOUR STORY HERE ⭐
story_idea = {
    'plot': '''
    A brave mouse named Max discovers a mysterious map in his grandmother's attic.
    The map leads to the legendary Golden Cheese, hidden deep in the Whispering Woods.
    
    Max meets a wise owl named Olivia who agrees to guide him on his journey.
    Together they face three challenges:
    1. Crossing the River of Riddles
    2. Navigating the Maze of Mirrors
    3. Befriending the Guardian of the Cheese
    
    Through courage, cleverness, and kindness, Max and Olivia succeed.
    But they discover the real treasure was the friendship they built along the way.
    ''',
    
    'target_age': '8-12',
    'themes': ['courage', 'adventure', 'friendship', 'wisdom'],
    'length': 'short',  # 'short', 'medium', or 'long'
    'art_style': 'children_book'  # 'children_book', 'cartoon', 'watercolor', 'line_art'
}

print(f"Plot: {story_idea['plot'][:100]}...")
print(f"Themes: {', '.join(story_idea['themes'])}")
print(f"Age: {story_idea['target_age']}")
print(f"Length: {story_idea['length']}")
print(f"Style: {story_idea['art_style']}")
print("="*70)

# Initialize orchestrator
orchestrator = DistributedOrchestrator(broker)

# Generate story
print("\n🚀 STARTING DISTRIBUTED STORY GENERATION")
print("="*70)
if torch.cuda.is_available():
    print("⏱️  Estimated time: 5-15 minutes (GPU)")
else:
    print("⏱️  Estimated time: 30-90 minutes (CPU)")
print("📊 Progress will be shown below...")
print("="*70)
print()

result = orchestrator.create_story(story_idea, timeout=1800)

# ============================================
# STEP 6: DISPLAY RESULTS
# ============================================

print("\n" + "="*70)
if result['status'] == 'complete':
    print("✅ STORY GENERATION COMPLETE!")
    print("="*70)
    
    metadata = result.get('metadata', {})
    print(f"\n📊 Story Statistics:")
    print(f"   Title: {metadata.get('title', 'Untitled Story')}")
    print(f"   Chapters: {metadata.get('chapters', 'N/A')}")
    print(f"   Illustrations: {metadata.get('images', 'N/A')}")
    print(f"   Pages: {metadata.get('page_count', 'N/A')}")
    
    publications = result.get('publications', {})
    print(f"\n📁 Output Files:")
    for format_type, filepath in publications.items():
        print(f"   {format_type.upper()}: {filepath}")
    
    # Download links
    from IPython.display import FileLink, display
    
    print("\n📥 DOWNLOAD YOUR STORY:")
    print("="*70)
    
    if 'pdf' in publications:
        print("\n📄 PDF (Main Output):")
        display(FileLink(publications['pdf']))
    
    if 'html' in publications:
        print("\n🌐 HTML (Preview):")
        display(FileLink(publications['html']))
    
    print("\n🎉 Your illustrated story book is ready!")
    
else:
    print("❌ STORY GENERATION FAILED")
    print("="*70)
    print(f"Status: {result.get('status', 'unknown')}")
    print(f"Message: {result.get('message', 'Unknown error')}")
    
    # Show message history for debugging
    correlation_id = result.get('correlation_id')
    if correlation_id:
        print("\n📨 Message History (for debugging):")
        history = orchestrator.get_message_history(correlation_id)
        for msg in history:
            print(f"  {msg['sender']} → {msg['receiver']}: {msg['content'].get('action', 'N/A')}")

print("\n" + "="*70)
print("✨ DONE!")
print("="*70)

# ============================================
# BONUS: CREATE MULTIPLE STORIES
# ============================================

# Uncomment to generate multiple stories in one session:
"""
print("\n\n" + "="*70)
print("📚 BONUS: CREATING MULTIPLE STORIES")
print("="*70)

story_ideas = [
    {
        'plot': 'A shy turtle learns to swim and makes new friends',
        'themes': ['courage', 'friendship'],
        'length': 'short'
    },
    {
        'plot': 'Kids start a recycling club to save their park',
        'themes': ['environment', 'teamwork'],
        'length': 'short'
    },
    {
        'plot': 'A robot learns about emotions and feelings',
        'themes': ['friendship', 'empathy'],
        'length': 'short'
    }
]

results = []
for i, idea in enumerate(story_ideas, 1):
    print(f"\n{'='*70}")
    print(f"📖 Story {i}/{len(story_ideas)}: {idea['plot'][:50]}...")
    print(f"{'='*70}")
    
    result = orchestrator.create_story(idea)
    results.append(result)
    
    if result['status'] == 'complete':
        print(f"✅ Story {i} complete!")
        display(FileLink(result['publications']['pdf']))
    else:
        print(f"❌ Story {i} failed: {result.get('message')}")

print(f"\n🎉 Generated {len([r for r in results if r['status'] == 'complete'])} stories!")
"""
