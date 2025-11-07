# Google Colab Setup Guide

This guide will help you run the AI Story Agents web interface on Google Colab with GPU acceleration.

## 🚀 Quick Start (Copy-Paste into Colab)

### Step 1: Setup and Installation

```python
# Clone the repository (or upload your files)
!git clone <your-repo-url> AI-Story-Agents
# OR if you have files in Google Drive:
# from google.colab import drive
# drive.mount('/content/drive')
# %cd /content/drive/MyDrive/AI-Story-Agents

%cd AI-Story-Agents

# Install dependencies
!pip install -q -r requirements.txt

# Verify GPU is available
import torch
print(f"GPU Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")
```

### Step 2: Launch Web Interface

```python
# Import and launch the web interface
from web_interface import StoryWebInterface

# Create interface with share=True for public link
web_interface = StoryWebInterface(config_path='config/agents_config.yaml')
web_interface.launch(share=True, server_port=7860)
```

**That's it!** Click the public URL (gradio.live link) to access your web interface.

---

## 📋 Complete Colab Notebook Template

Copy this entire code block into a new Colab notebook:

```python
# ============================================
# AI STORY AGENTS - GOOGLE COLAB SETUP
# ============================================

# 1. Check GPU
import torch
print("=" * 60)
print("🔍 Checking GPU Availability...")
print("=" * 60)
print(f"GPU Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
else:
    print("⚠️  No GPU detected. Go to Runtime > Change runtime type > GPU")
print("=" * 60)

# 2. Clone Repository
print("\n📥 Cloning repository...")
!git clone https://github.com/YOUR_USERNAME/AI-Story-Agents.git
%cd AI-Story-Agents

# 3. Install Dependencies
print("\n📦 Installing dependencies...")
!pip install -q -r requirements.txt

# 4. Configure for Colab (Optional - reduce memory usage)
import yaml

config_path = 'config/agents_config.yaml'
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Use smaller models for faster loading (optional)
# config['author']['model_name'] = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
# config['illustrator']['num_inference_steps'] = 30  # Faster generation

with open(config_path, 'w') as f:
    yaml.dump(config, f)

print("✅ Configuration updated for Colab")

# 5. Launch Web Interface
print("\n🚀 Launching Web Interface...")
print("=" * 60)
print("Click the gradio.live link below to access your app!")
print("=" * 60)

from web_interface import StoryWebInterface

web_interface = StoryWebInterface(config_path='config/agents_config.yaml')
web_interface.launch(share=True, server_port=7860)
```

---

## 🎯 Alternative: Direct Python Execution

If you prefer not to use the web interface:

```python
from orchestrator.coordinator import StoryOrchestrator

# Initialize
orchestrator = StoryOrchestrator()

# Create story
story_idea = {
    'plot': 'A brave mouse goes on an adventure to find magical cheese',
    'target_age': '8-12',
    'themes': ['courage', 'friendship', 'adventure'],
    'length': 'short',
    'art_style': 'children_book'
}

# Generate
result = orchestrator.create_story(story_idea)

# Download PDF
from google.colab import files
if result['status'] == 'complete':
    pdf_path = result['publications']['pdf']
    files.download(pdf_path)
```

---

## 💾 Using Google Drive

To save outputs to Google Drive:

```python
# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Update output directory in config
import yaml

with open('config/agents_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

config['output_dir'] = '/content/drive/MyDrive/AI-Story-Outputs'

with open('config/agents_config.yaml', 'w') as f:
    yaml.dump(config, f)

# Now launch the interface
from web_interface import StoryWebInterface
web_interface = StoryWebInterface(config_path='config/agents_config.yaml')
web_interface.launch(share=True)
```

---

## ⚙️ Configuration Tips for Colab

### Memory Optimization

If you run out of memory, edit `config/agents_config.yaml`:

```yaml
author:
  model_name: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Smaller model
  load_in_8bit: true

illustrator:
  num_inference_steps: 30  # Faster, uses less memory
  width: 512
  height: 512
```

### Speed Optimization

```yaml
illustrator:
  num_inference_steps: 25  # Minimum for decent quality
  guidance_scale: 7.0

performance:
  batch_size: 1
  cache_models: true
```

---

## 🔧 Troubleshooting

### Out of Memory Error
```python
# Clear GPU memory
import torch
torch.cuda.empty_cache()

# Restart runtime: Runtime > Restart runtime
```

### Model Download Issues
```python
# Models download automatically from HuggingFace
# First run will take 10-15 minutes
# Subsequent runs will be faster (models are cached)

# Check download progress
!ls -lh ~/.cache/huggingface/hub/
```

### Connection Timeout
```python
# Colab sessions timeout after 12 hours of inactivity
# Keep the tab open or use Colab Pro for longer sessions
```

---

## 📊 Expected Performance

- **First Run**: 10-15 minutes (model downloads)
- **Story Generation**: 5-15 minutes depending on length
- **GPU**: T4 or better recommended
- **Memory**: 12GB+ GPU memory ideal

---

## 🎨 Web Interface Features

The web interface provides:

- ✅ User-friendly form for story inputs
- ✅ Real-time progress updates
- ✅ PDF download directly from browser
- ✅ Preview of story statistics
- ✅ Demo story button for quick testing
- ✅ Mobile-responsive design

---

## 📱 Sharing Your App

The `share=True` parameter creates a public link that:

- Works for 72 hours
- Can be shared with anyone
- No authentication required
- Automatically handles HTTPS

Perfect for demos and sharing with friends!

---

## 🆘 Support

- Check the main README.md for detailed documentation
- Review QUICKSTART.md for usage examples
- Inspect config/agents_config.yaml for all options

---

## 🎉 Enjoy Creating Stories!

Your AI Story Agents are ready to collaborate and create amazing illustrated children's books!
