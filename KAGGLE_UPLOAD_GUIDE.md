# Kaggle Setup Guide - Upload Method

Since Kaggle has network restrictions, the best approach is to upload the code as a dataset.

## 🎯 Method 1: Upload as Kaggle Dataset (Recommended)

### Step 1: Prepare Local Files

On your local machine:

```bash
cd /Users/vbawa/Downloads/Story\ Writing

# Create a clean zip without git files
zip -r AI-Story-Agents-kaggle.zip AI-Story-Agents \
  -x "*.git*" \
  -x "*__pycache__*" \
  -x "*.pyc" \
  -x "*/output/*" \
  -x "*.DS_Store"
```

### Step 2: Create Kaggle Dataset

1. Go to https://www.kaggle.com/datasets
2. Click **"New Dataset"**
3. Click **"Upload"** → Select `AI-Story-Agents-kaggle.zip`
4. Title: `AI Story Agents`
5. Make it **Public** or **Private**
6. Click **"Create"**

### Step 3: Use in Kaggle Notebook

Create a new notebook and add your dataset:

1. **New Notebook** → Enable **GPU T4 x2**
2. **Right sidebar** → **Add Data** → Search for your dataset
3. **Add** it to the notebook

Then run this code:

```python
# ============================================
# KAGGLE NOTEBOOK - WITH DATASET
# ============================================

import torch
print("="*70)
print("🔍 GPU CHECK")
print("="*70)
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")
print("="*70)

# Install dependencies
print("\n📦 Installing dependencies...")
get_ipython().system('pip install -q transformers diffusers accelerate pillow pyyaml reportlab')

# Copy from dataset to working directory
import shutil
import os

print("\n📥 Copying code from dataset...")
dataset_path = '/kaggle/input/ai-story-agents/AI-Story-Agents'  # Adjust path

if os.path.exists(dataset_path):
    # Copy all files
    for item in os.listdir(dataset_path):
        src = os.path.join(dataset_path, item)
        dst = os.path.join('/kaggle/working', item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)
    print("✅ Code copied!")
else:
    print(f"❌ Dataset not found at {dataset_path}")
    print("   Make sure you added the dataset to this notebook")

# Change to working directory
os.chdir('/kaggle/working')

# Import orchestrator
from orchestrator.coordinator import StoryOrchestrator

print("\n🎬 Initializing AI Story Agents...")
orchestrator = StoryOrchestrator()
print("✅ Agents ready!")

# Create story
story_idea = {
    'plot': '''
    A brave mouse named Max discovers a mysterious map.
    He teams up with a wise owl to find the legendary Golden Cheese.
    Through courage and friendship, they overcome challenges.
    ''',
    'target_age': '8-12',
    'themes': ['courage', 'adventure', 'friendship'],
    'length': 'short',
    'art_style': 'children_book'
}

print("\n🚀 Starting story generation...")
print("⏱️  Estimated time: 5-15 minutes on GPU")
print("="*70)

result = orchestrator.create_story(story_idea)

# Display result
if result['status'] == 'complete':
    print("\n✅ STORY COMPLETE!")
    print(f"Chapters: {result['metadata']['chapters']}")
    print(f"Images: {result['metadata']['images']}")
    
    from IPython.display import FileLink
    print("\n📥 Download your PDF:")
    display(FileLink(result['publications']['pdf']))
else:
    print(f"\n❌ Failed: {result.get('message')}")
```

---

## 🎯 Method 2: Direct GitHub Clone (If Internet Enabled)

If Kaggle internet is enabled:

```python
# Enable Internet in Kaggle Settings first!

import torch
print(f"GPU: {torch.cuda.get_device_name(0)}")

# Clone repository
get_ipython().system('git clone https://github.com/chanderbawa/AI-Story-Agents.git')
get_ipython().system('cd AI-Story-Agents')

# Install dependencies
get_ipython().system('pip install -q -r AI-Story-Agents/requirements.txt')

# Change directory
import os
os.chdir('AI-Story-Agents')

# Run
from orchestrator.coordinator import StoryOrchestrator

orchestrator = StoryOrchestrator()

story_idea = {
    'plot': 'Your story here',
    'themes': ['friendship', 'courage'],
    'length': 'short'
}

result = orchestrator.create_story(story_idea)

if result['status'] == 'complete':
    from IPython.display import FileLink
    display(FileLink(result['publications']['pdf']))
```

---

## 🎯 Method 3: Monolithic Mode (Simplest)

If you just want to generate stories without the distributed system:

```python
import torch
print(f"GPU: {torch.cuda.get_device_name(0)}")

# Install
get_ipython().system('pip install -q transformers diffusers accelerate pillow pyyaml reportlab')

# Download only essential files
import urllib.request
import os

files = {
    'agents/__init__.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/agents/__init__.py',
    'agents/base_agent.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/agents/base_agent.py',
    'agents/author_agent.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/agents/author_agent.py',
    'agents/illustrator_agent.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/agents/illustrator_agent.py',
    'agents/publisher_agent.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/agents/publisher_agent.py',
    'orchestrator/__init__.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/orchestrator/__init__.py',
    'orchestrator/coordinator.py': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/orchestrator/coordinator.py',
    'config/agents_config.yaml': 'https://raw.githubusercontent.com/chanderbawa/AI-Story-Agents/main/config/agents_config.yaml',
}

for filepath, url in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"✅ {filepath}")
    except Exception as e:
        print(f"❌ {filepath}")

# Use it
from orchestrator.coordinator import StoryOrchestrator

orchestrator = StoryOrchestrator()

story_idea = {
    'plot': 'A brave mouse goes on an adventure',
    'themes': ['courage', 'friendship'],
    'length': 'short'
}

result = orchestrator.create_story(story_idea)

if result['status'] == 'complete':
    from IPython.display import FileLink
    display(FileLink(result['publications']['pdf']))
```

---

## 🔧 Troubleshooting

### "Temporary failure in name resolution"

**Cause**: Kaggle internet is disabled

**Solution**: 
1. Settings → Internet → **ON**
2. Or use Method 1 (Upload as Dataset)

### "No module named 'distributed'"

**Cause**: Files not downloaded

**Solution**: Use Method 1 (Dataset upload) - most reliable

### "Out of memory"

**Cause**: GPU memory exhausted

**Solution**: Use shorter stories or reduce image size:
```python
# Before creating orchestrator
import yaml
with open('config/agents_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

config['illustrator']['width'] = 512
config['illustrator']['height'] = 512

with open('config/agents_config.yaml', 'w') as f:
    yaml.dump(config, f)
```

---

## 📊 Comparison

| Method | Reliability | Setup Time | Best For |
|--------|-------------|------------|----------|
| **Dataset Upload** | ⭐⭐⭐⭐⭐ | 5 min | Production use |
| **Git Clone** | ⭐⭐⭐ | 2 min | Quick tests |
| **Direct Download** | ⭐⭐ | 2 min | Simple stories |

---

## ✅ Recommended Workflow

**For Kaggle:**

1. **First Time**: Upload as dataset (Method 1)
2. **Every Session**: Add dataset to notebook
3. **Generate**: Run the code above

**Benefits:**
- ✅ No network issues
- ✅ Faster setup
- ✅ Reusable across notebooks
- ✅ Works even with internet disabled

---

## 🎯 Quick Start (Copy-Paste)

**After uploading dataset:**

```python
import torch, shutil, os
from IPython.display import FileLink

print(f"GPU: {torch.cuda.get_device_name(0)}")

# Install
get_ipython().system('pip install -q transformers diffusers accelerate pillow pyyaml reportlab')

# Copy from dataset
shutil.copytree('/kaggle/input/ai-story-agents/AI-Story-Agents', '/kaggle/working/code', dirs_exist_ok=True)
os.chdir('/kaggle/working/code')

# Generate
from orchestrator.coordinator import StoryOrchestrator
orchestrator = StoryOrchestrator()

result = orchestrator.create_story({
    'plot': 'A brave mouse goes on an adventure to find magical cheese',
    'themes': ['courage', 'friendship'],
    'length': 'short'
})

# Download
if result['status'] == 'complete':
    display(FileLink(result['publications']['pdf']))
```

That's it! 🎉
