# Running AI Story Agents on CPU

Complete guide for running the AI Story Agents on CPU without GPU.

## ⚡ Quick Start

```bash
# Navigate to project directory
cd /Users/vbawa/Downloads/Story\ Writing/AI-Story-Agents

# Launch CPU-optimized version
python app_cpu.py
```

Then open your browser to **http://localhost:7860**

---

## 📋 Prerequisites

### System Requirements

**Minimum:**
- 16GB RAM
- 4-core CPU
- 20GB free disk space
- macOS, Windows, or Linux

**Recommended:**
- 32GB RAM
- 8-core CPU
- SSD storage
- Latest Python 3.11+

### Check Your System

```bash
# Check Python version
python3 --version

# Check available RAM
# macOS:
sysctl hw.memsize

# Linux:
free -h

# Windows:
systeminfo | findstr Memory
```

---

## 🚀 Installation

### Step 1: Verify Dependencies

```bash
# Check if dependencies are installed
pip3 list | grep -E "(torch|transformers|diffusers|gradio)"
```

If missing, install:

```bash
pip3 install -r requirements.txt
```

### Step 2: Verify Installation

```bash
# Test that everything works
python3 test_web_interface.py
```

---

## 🎯 Running the Application

### Option 1: Web Interface (Recommended)

```bash
# Use CPU-optimized launcher
python3 app_cpu.py
```

**What this does:**
- Uses TinyLlama (1.1B) instead of Mistral (7B)
- Reduces image generation steps (25 instead of 50)
- Generates smaller images (512x512 instead of 768x1024)
- Forces CPU usage

### Option 2: Command Line

```bash
# Create a story via CLI
python3 main.py --plot "Your story idea" --length short
```

### Option 3: Custom Configuration

```bash
# Use your own config
python3 web_interface.py --config config/agents_config_cpu.yaml
```

---

## ⏱️ Performance Expectations

### Generation Times (CPU)

| Story Length | Text Generation | Image Generation | Total Time |
|--------------|----------------|------------------|------------|
| Short (3ch)  | 10-15 min      | 20-30 min        | 30-45 min  |
| Medium (5ch) | 15-20 min      | 30-40 min        | 45-60 min  |
| Long (8ch)   | 20-30 min      | 40-60 min        | 60-90 min  |

### What Affects Speed

**Faster:**
- More CPU cores
- More RAM
- SSD storage
- Fewer background apps
- Smaller models

**Slower:**
- Older CPU
- Limited RAM (< 16GB)
- HDD storage
- Many background apps
- Larger models

---

## 🔧 Optimization Tips

### 1. Close Unnecessary Applications

```bash
# Free up RAM before running
# Close: browsers, IDEs, video players, etc.
```

### 2. Use Smaller Models

The CPU config already uses TinyLlama, but you can go even smaller:

```yaml
# In config/agents_config_cpu.yaml
author:
  model_name: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Already optimized
```

### 3. Reduce Image Quality

```yaml
# In config/agents_config_cpu.yaml
illustrator:
  num_inference_steps: 20  # Reduce from 25 (faster, lower quality)
  width: 384               # Reduce from 512
  height: 384
```

### 4. Generate Fewer Images

```yaml
# In config/agents_config_cpu.yaml
quality:
  images_per_chapter: 1  # Reduce from 2
```

### 5. Use Short Stories

Start with short stories (3 chapters) to test the system before attempting longer ones.

---

## 🐛 Troubleshooting

### Out of Memory Error

**Symptoms:**
```
RuntimeError: [enforce fail at alloc_cpu.cpp:...] . DefaultCPUAllocator: can't allocate memory
```

**Solutions:**

1. **Close other applications**
   ```bash
   # Free up RAM
   ```

2. **Use even smaller models**
   ```yaml
   author:
     model_name: "distilgpt2"  # Much smaller
   ```

3. **Generate one chapter at a time**
   ```yaml
   performance:
     save_intermediate: true
   ```

4. **Reduce image size**
   ```yaml
   illustrator:
     width: 256
     height: 256
   ```

### Very Slow Generation

**Normal behavior:**
- CPU generation is 10-20x slower than GPU
- First run downloads models (~15GB)
- Subsequent runs are faster (models cached)

**Speed improvements:**

1. **Use the demo first** to cache models:
   ```bash
   python3 main.py --demo
   ```

2. **Monitor progress** in terminal output

3. **Be patient** - it's working, just slowly!

### Models Not Downloading

**Check internet connection:**
```bash
# Test HuggingFace access
curl -I https://huggingface.co
```

**Check cache location:**
```bash
# Models download to:
ls -lh ~/.cache/huggingface/hub/
```

**Manual download** (if needed):
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Download models manually
model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
```

### Port Already in Use

```bash
# Find what's using port 7860
lsof -i :7860

# Kill the process
kill -9 <PID>

# Or use a different port
python3 web_interface.py --port 8080
```

---

## 💡 Best Practices for CPU

### 1. Start Small

```bash
# Test with demo first
python3 main.py --demo
```

### 2. Monitor Resources

**macOS:**
```bash
# Open Activity Monitor
open -a "Activity Monitor"
```

**Linux:**
```bash
# Monitor CPU and RAM
htop
```

**Windows:**
```bash
# Open Task Manager
taskmgr
```

### 3. Plan Ahead

- Generate stories overnight or during breaks
- Don't expect instant results
- CPU mode is for convenience, not speed

### 4. Save Progress

The CPU config automatically saves intermediate results:
```yaml
performance:
  save_intermediate: true
```

Check `output/publications/` for partial results.

---

## 📊 CPU vs GPU Comparison

| Feature | CPU | GPU (T4) |
|---------|-----|----------|
| Setup | Easy | Requires CUDA |
| Cost | Free | Cloud costs |
| Speed | Slow (30-90 min) | Fast (5-15 min) |
| Quality | Same | Same |
| Reliability | High | Depends on cloud |

---

## 🎨 Example: Creating Your First Story

### Step 1: Launch

```bash
python3 app_cpu.py
```

### Step 2: Open Browser

Navigate to: **http://localhost:7860**

### Step 3: Fill Form

```
Plot: A brave mouse goes on an adventure to find magical cheese
Themes: courage, adventure, friendship
Age: 8-12
Length: Short  ← Start with SHORT!
Style: Children Book
```

### Step 4: Click "Create Story"

### Step 5: Wait Patiently

- Watch terminal for progress logs
- Keep browser tab open
- Don't close terminal
- Expect 30-45 minutes for short story

### Step 6: Download PDF

Once complete, click the download button!

---

## 🔍 Monitoring Progress

### Terminal Output

Watch for these messages:

```
INFO:Orchestrator:🎬 STARTING STORY CREATION WORKFLOW
INFO:Orchestrator:📝 PHASE 1: STORY CREATION
INFO:Agent.AuthorAgent:Writing chapter 1...
INFO:Agent.AuthorAgent:Writing chapter 2...
INFO:Agent.AuthorAgent:Writing chapter 3...
INFO:Orchestrator:🎨 PHASE 2: ILLUSTRATION GENERATION
INFO:Agent.IllustratorAgent:Generating image 1/6...
INFO:Agent.IllustratorAgent:Generating image 2/6...
...
INFO:Orchestrator:📚 PHASE 3: PUBLICATION ASSEMBLY
INFO:Agent.PublisherAgent:Creating PDF...
INFO:Orchestrator:✅ SUCCESS! Your story is ready!
```

### Browser Interface

- Progress bar shows overall completion
- Status messages update in real-time
- PDF appears when complete

---

## 🆘 Getting Help

### Check Logs

```bash
# Run with verbose logging
python3 app_cpu.py 2>&1 | tee story_generation.log
```

### Test Components

```bash
# Test web interface
python3 test_web_interface.py

# Test with demo
python3 main.py --demo
```

### Common Issues

1. **"Out of memory"** → Close apps, use smaller models
2. **"Too slow"** → Normal for CPU, be patient
3. **"Models not loading"** → Check internet, wait for download
4. **"Port in use"** → Use different port or kill process

---

## 🚀 Alternative: Use GPU in Cloud

If CPU is too slow, consider:

1. **Google Colab** (Free GPU)
   - See COLAB_SETUP.md
   - T4 GPU included
   - Much faster

2. **Local GPU** (if you have one)
   ```bash
   # Use regular config
   python3 app.py
   ```

---

## 📝 Summary

**CPU Mode is:**
- ✅ Easy to set up
- ✅ Works on any computer
- ✅ No cloud costs
- ✅ Same quality output
- ⚠️ Much slower (30-90 min vs 5-15 min)

**Best For:**
- Testing the system
- Occasional story generation
- No GPU available
- Learning how it works

**Not Ideal For:**
- Frequent use
- Multiple stories
- Time-sensitive projects
- Production use

---

**Ready to create your first story on CPU? Run `python3 app_cpu.py` and get started!** 🚀
