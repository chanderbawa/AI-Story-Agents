# AI Story Agents - Quick Reference Card

## 🚀 Getting Started (30 seconds)

### Local Machine
```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:7860
```

### Google Colab
```python
!git clone <repo-url> AI-Story-Agents && cd AI-Story-Agents
!pip install -q -r requirements.txt
from web_interface import StoryWebInterface
StoryWebInterface().launch(share=True)
```

---

## 📝 Command Cheat Sheet

### Web Interface
```bash
python app.py                              # Launch web UI
python web_interface.py --port 8080        # Custom port
python web_interface.py --share            # Public link
python web_interface.py --config my.yaml   # Custom config
```

### CLI Interface
```bash
python main.py --plot "Your story"         # Create story
python main.py --interactive               # Interactive mode
python main.py --demo                      # Run demo
python main.py --help                      # Show all options
```

### Python API
```python
from orchestrator.coordinator import StoryOrchestrator

orchestrator = StoryOrchestrator()
result = orchestrator.create_story({
    'plot': "Your story idea",
    'target_age': "8-12",
    'themes': ['friendship', 'courage'],
    'length': 'short',
    'art_style': 'children_book'
})
print(result['publications']['pdf'])
```

---

## 🎨 Story Parameters

### Plot
- **What**: Main story idea/concept
- **Example**: "A shy kid discovers they can talk to animals"
- **Tips**: Be specific, include conflict, mention characters

### Themes (comma-separated)
- friendship, courage, kindness
- adventure, discovery, perseverance
- family, honesty, teamwork
- nature, creativity, self-confidence

### Target Age
- **5-7**: Simple vocabulary, basic concepts
- **8-12**: Complex plots, chapter structure
- **10-14**: Deeper themes, longer narratives

### Length
- **Short**: 3 chapters, ~10-15 pages, 5-10 min
- **Medium**: 5 chapters, ~20-30 pages, 10-15 min
- **Long**: 8 chapters, ~40-50 pages, 15-25 min

### Art Style
- **Children Book**: Classic storybook illustrations
- **Cartoon**: Fun, animated style
- **Watercolor**: Soft, artistic look
- **Line Art**: Simple, clean drawings

---

## ⚙️ Configuration Quick Edit

Edit `config/agents_config.yaml`:

### Faster Generation (Lower Quality)
```yaml
illustrator:
  num_inference_steps: 25
  width: 512
  height: 512
```

### Memory Optimization
```yaml
author:
  load_in_8bit: true
  model_name: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
```

### Better Quality (Slower)
```yaml
illustrator:
  num_inference_steps: 50
  width: 768
  height: 1024
  guidance_scale: 8.0
```

---

## 🔧 Troubleshooting

### Out of Memory
```bash
# Clear GPU cache
python -c "import torch; torch.cuda.empty_cache()"

# Use smaller models in config
# Enable load_in_8bit: true
```

### Port Already in Use
```bash
# Find process using port
lsof -i :7860

# Use different port
python app.py --port 8080
```

### Slow Generation
```yaml
# In config/agents_config.yaml
illustrator:
  num_inference_steps: 25  # Reduce from 50
```

### Models Not Downloading
```bash
# Check internet connection
# Models download to ~/.cache/huggingface/
# First run takes 10-15 minutes
```

---

## 📁 File Locations

### Input
- `config/agents_config.yaml` - Configuration
- `examples/` - Example scripts

### Output
- `output/publications/` - Generated PDFs
- `output/publications/*.pdf` - Story PDFs
- `output/publications/*.html` - HTML versions
- `output/publications/img_*.png` - Illustrations

### Logs
- Console output shows progress
- Agent status updates in real-time

---

## 🎯 Common Use Cases

### Quick Test
```bash
python main.py --demo
```

### Custom Story
```bash
python main.py --plot "Your idea" --themes adventure courage --age 8-12
```

### Web Interface
```bash
python app.py
# Fill form in browser
```

### Colab Notebook
```python
# See COLAB_SETUP.md for full code
```

---

## 📊 Expected Performance

### Hardware Requirements
- **Minimum**: 16GB RAM, CPU only (slow)
- **Recommended**: 12GB+ GPU, 16GB RAM
- **Optimal**: 24GB+ GPU, 32GB RAM

### Generation Times (GPU)
- Short: 5-10 minutes
- Medium: 10-15 minutes
- Long: 15-25 minutes

### Generation Times (CPU)
- Short: 30-45 minutes
- Medium: 45-60 minutes
- Long: 60-90 minutes

---

## 🐛 Debug Commands

### Check GPU
```python
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```

### Test Interface
```bash
python test_web_interface.py
```

### Verify Installation
```bash
pip list | grep -E "(torch|transformers|diffusers|gradio)"
```

### Check Models
```bash
ls -lh ~/.cache/huggingface/hub/
```

---

## 📚 Documentation Links

- **README.md** - Project overview
- **QUICKSTART.md** - Basic usage
- **COLAB_SETUP.md** - Google Colab guide
- **WEB_INTERFACE_GUIDE.md** - Web UI details
- **ARCHITECTURE.md** - System architecture
- **SUMMARY.md** - What's been added

---

## 🎨 Example Stories

### Adventure
```
Plot: A young explorer discovers a hidden world beneath their backyard
Themes: courage, curiosity, friendship
Age: 8-12, Length: Medium, Style: Children Book
```

### Educational
```
Plot: Kids learn about recycling by cleaning up their neighborhood park
Themes: environment, teamwork, responsibility
Age: 5-7, Length: Short, Style: Cartoon
```

### Fantasy
```
Plot: A shy bookworm finds a magical library where characters come to life
Themes: imagination, confidence, adventure
Age: 10-14, Length: Long, Style: Watercolor
```

---

## 💡 Pro Tips

1. **First Run**: Takes longer (model downloads)
2. **GPU**: Significantly faster than CPU
3. **Themes**: 2-4 themes work best
4. **Plot**: More detail = better results
5. **Length**: Start with short stories
6. **Style**: Match style to content
7. **Age**: Consider vocabulary level
8. **Colab**: Use share=True for public link
9. **Config**: Backup before editing
10. **Output**: Check output/publications/

---

## 🆘 Quick Help

### Interface won't start
- Check port availability
- Verify dependencies installed
- Try different port

### Story generation fails
- Check GPU/memory
- Reduce inference steps
- Use smaller models

### PDF not downloading
- Check output directory
- Verify file permissions
- Check disk space

### Slow performance
- Enable GPU
- Reduce image size
- Use 8-bit loading

---

## 📞 Support Resources

- Check error messages in console
- Review configuration file
- Test with demo mode first
- Verify GPU availability
- Check model cache location

---

**Quick Start**: `python app.py` → Open browser → Create story! 🚀
