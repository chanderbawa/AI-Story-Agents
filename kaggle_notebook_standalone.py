"""
Kaggle Notebook - Standalone AI Story Agents

⚠️  IMPORTANT: This requires uploading code as a Kaggle Dataset first!
See KAGGLE_UPLOAD_GUIDE.md for instructions.

QUICK SETUP:
1. Upload AI-Story-Agents as a Kaggle Dataset (one-time)
2. Enable GPU: Right sidebar → Accelerator → GPU T4 x2
3. Add your dataset: Right sidebar → Add Data → Your dataset
4. Copy this entire code
5. Paste into a Kaggle cell
6. Run!

Alternative: Enable Internet in Settings if you want to download directly.
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
print("⏱️  This may take 2-3 minutes...")

# Install packages one by one to handle failures
packages = [
    'transformers',
    'diffusers', 
    'accelerate',
    'pillow',
    'pyyaml',
    'reportlab'
]

for pkg in packages:
    try:
        get_ipython().system(f'pip install -q {pkg}')
        print(f"✅ {pkg}")
    except:
        print(f"⚠️  {pkg} - using pre-installed version")

print("\n✅ Dependencies ready!")

# ============================================
# STEP 3: SETUP CODE
# ============================================

print("\n📁 Setting up code...")

import os
import shutil

# Check if dataset is available
dataset_paths = [
    '/kaggle/input/ai-story-agents/AI-Story-Agents',
    '/kaggle/input/ai-story-agents',
    '/kaggle/input/aistoryagents/AI-Story-Agents'
]

dataset_found = False
for path in dataset_paths:
    if os.path.exists(path):
        print(f"✅ Found dataset at: {path}")
        # Copy to working directory
        if os.path.isdir(path):
            for item in os.listdir(path):
                src = os.path.join(path, item)
                dst = os.path.join('/kaggle/working', item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
        dataset_found = True
        break

if not dataset_found:
    print("⚠️  Dataset not found!")
    print("   Please add your AI-Story-Agents dataset to this notebook")
    print("   See KAGGLE_UPLOAD_GUIDE.md for instructions")
    raise Exception("Dataset not found. Please upload and add the dataset first.")

os.chdir('/kaggle/working')
print("✅ Code ready!")

# ============================================
# STEP 4: INITIALIZE ORCHESTRATOR
# ============================================

print("\n🎬 Initializing AI Story Agents...")

from orchestrator.coordinator import StoryOrchestrator

# Initialize orchestrator
orchestrator = StoryOrchestrator()

print("✅ Agents ready!")
print("="*70)

# ============================================
# STEP 4: CREATE YOUR STORY
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

# Generate story
print("\n🚀 STARTING STORY GENERATION")
print("="*70)
if torch.cuda.is_available():
    print("⏱️  Estimated time: 5-15 minutes (GPU)")
else:
    print("⏱️  Estimated time: 30-90 minutes (CPU)")
print("📊 Progress will be shown below...")
print("="*70)
print()

result = orchestrator.create_story(story_idea)

# ============================================
# STEP 5: DISPLAY RESULTS
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
