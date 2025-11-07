# Web Interface Guide

Complete guide for using the AI Story Agents web interface.

## 🚀 Quick Start

### Local Machine

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch web interface
python app.py

# 3. Open browser to http://localhost:7860
```

### Google Colab

See [COLAB_SETUP.md](COLAB_SETUP.md) for detailed Colab instructions.

---

## 🌐 Web Interface Overview

The web interface provides a user-friendly way to create illustrated children's books without writing any code.

### Features

- **📝 Story Input Form**: Enter plot, themes, age range, and preferences
- **🎨 Art Style Selection**: Choose from multiple illustration styles
- **📊 Real-Time Progress**: See updates as your story is being created
- **📥 PDF Download**: Download your completed book directly
- **🎬 Demo Mode**: Try a pre-configured example story
- **📱 Mobile Friendly**: Works on all devices

---

## 📝 Using the Interface

### 1. Story Plot/Idea

Enter your story concept in the text area. Be as detailed or simple as you like:

**Examples:**
- Simple: "A brave mouse goes on an adventure"
- Detailed: "A shy 9-year-old discovers they can talk to animals and uses this gift to help save the school garden from developers"
- Character-focused: "A plump, witty kid uses humor and kindness to make friends at a new school"

**Tips:**
- Include main character traits
- Mention the central conflict or challenge
- Consider the setting
- Think about the lesson or theme

### 2. Themes

Enter comma-separated themes for your story:

**Common Themes:**
- friendship, courage, kindness
- adventure, discovery, perseverance
- family, honesty, teamwork
- nature, creativity, self-confidence

### 3. Target Age

Select the appropriate age range:
- **5-7**: Simple vocabulary, shorter sentences
- **8-12**: More complex plots, chapter structure
- **10-14**: Deeper themes, longer narratives

### 4. Story Length

Choose the length:
- **Short**: 3 chapters (~10-15 pages)
- **Medium**: 5 chapters (~20-30 pages)
- **Long**: 8 chapters (~40-50 pages)

⏱️ **Generation Time:**
- Short: 5-10 minutes
- Medium: 10-15 minutes
- Long: 15-25 minutes

### 5. Art Style

Select the illustration style:
- **Children Book**: Classic storybook illustrations
- **Cartoon**: Fun, animated style
- **Watercolor**: Soft, artistic look
- **Line Art**: Simple, clean drawings

---

## 🎬 Demo Mode

Click the "Try Demo" button to generate a pre-configured example story. This is perfect for:
- Testing the system
- Seeing what's possible
- Learning how the agents work together

The demo story features Leo, a witty kid who makes friends at a new school.

---

## 📥 Downloading Your Story

Once generation is complete:

1. **View Statistics**: See chapter count, illustrations, and page count
2. **Download PDF**: Click the download button to get your PDF
3. **Files Location**: PDFs are saved to `output/publications/`

### Output Files

Your story generates:
- `story_title.pdf` - Complete illustrated book
- `story_title.html` - Web version (if enabled)
- `img_*.png` - Individual illustrations

---

## ⚙️ Advanced Options

### Custom Configuration

To customize agent behavior, edit `config/agents_config.yaml`:

```yaml
# Example: Use smaller models for faster generation
author:
  model_name: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
  load_in_8bit: true

illustrator:
  num_inference_steps: 30  # Faster but lower quality
  width: 512
  height: 512
```

### Command Line Options

Launch with custom settings:

```bash
# Custom port
python web_interface.py --port 8080

# Create public share link
python web_interface.py --share

# Custom config file
python web_interface.py --config my_config.yaml
```

---

## 🔧 Troubleshooting

### Interface Won't Load

```bash
# Check if port is already in use
lsof -i :7860

# Try a different port
python web_interface.py --port 8080
```

### Story Generation Fails

**Common Issues:**

1. **Out of Memory**
   - Use smaller models in config
   - Enable 8-bit loading
   - Reduce image dimensions

2. **Model Download Timeout**
   - First run downloads ~15GB of models
   - Ensure stable internet connection
   - Models cache in `~/.cache/huggingface/`

3. **GPU Not Detected**
   - Check CUDA installation: `python -c "import torch; print(torch.cuda.is_available())"`
   - CPU mode works but is slower

### Slow Generation

**Speed Optimization:**

```yaml
# In config/agents_config.yaml
illustrator:
  num_inference_steps: 25  # Minimum for decent quality
  width: 512
  height: 512

performance:
  batch_size: 1
  cache_models: true
```

---

## 🌍 Deployment Options

### Local Network Access

Allow other devices on your network to access:

```bash
python web_interface.py --server-name 0.0.0.0
```

Then access from other devices using your computer's IP address.

### Public Deployment

For production deployment, consider:

1. **Hugging Face Spaces**: Free hosting for Gradio apps
2. **Google Cloud Run**: Serverless container deployment
3. **AWS/Azure**: Full control with VM instances

**Note:** GPU instances can be expensive. Consider:
- Using smaller models
- Implementing request queuing
- Setting usage limits

---

## 📊 Understanding the Output

### Story Statistics

After generation, you'll see:
- **Chapters**: Number of story chapters
- **Illustrations**: Total images generated
- **Pages**: Estimated page count in PDF

### Quality Indicators

The agents aim for:
- **Consistency**: Characters look the same across illustrations
- **Coherence**: Story flows naturally with proper pacing
- **Age-Appropriate**: Content matches target age range
- **Visual-Text Alignment**: Images support the narrative

---

## 🎨 Customizing the Interface

### Modify Appearance

Edit `web_interface.py` to customize:

```python
# Change theme
interface = gr.Blocks(theme=gr.themes.Monochrome())

# Custom CSS
css = """
.gradio-container {
    background: linear-gradient(to right, #ff6b6b, #4ecdc4);
}
"""
```

### Add New Features

The `StoryWebInterface` class can be extended:

```python
def add_custom_feature(self):
    # Your custom functionality
    pass
```

---

## 🔐 Security Considerations

### For Public Deployment

- Implement authentication (Gradio supports auth)
- Set rate limits to prevent abuse
- Monitor GPU usage and costs
- Validate user inputs
- Consider content moderation

### Example: Add Authentication

```python
interface.launch(
    auth=("username", "password"),
    share=True
)
```

---

## 📈 Performance Monitoring

### Track Usage

```python
# Add logging to track requests
import logging
logging.basicConfig(
    filename='story_requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
```

### Monitor Resources

```bash
# GPU usage
nvidia-smi -l 1

# Memory usage
watch -n 1 free -h
```

---

## 🎓 Best Practices

### For Best Results

1. **Be Specific**: Detailed plots lead to better stories
2. **Match Age Range**: Consider vocabulary and themes
3. **Choose Appropriate Length**: Start with short stories
4. **Test Styles**: Try different art styles for your content
5. **Iterate**: Generate multiple versions and pick the best

### For Efficient Generation

1. **Cache Models**: First run is slow, subsequent runs are faster
2. **Batch Similar Requests**: Generate multiple stories in one session
3. **Use Appropriate Hardware**: GPU significantly speeds up generation
4. **Optimize Config**: Balance quality vs. speed based on needs

---

## 🆘 Getting Help

### Resources

- **README.md**: Project overview and features
- **QUICKSTART.md**: Basic usage guide
- **COLAB_SETUP.md**: Google Colab instructions
- **config/agents_config.yaml**: All configuration options

### Common Questions

**Q: How long does generation take?**
A: 5-25 minutes depending on story length and hardware.

**Q: Can I run without GPU?**
A: Yes, but it will be significantly slower (30-60 minutes).

**Q: Can I customize the agents?**
A: Yes, edit the agent files in the `agents/` directory.

**Q: What models are used?**
A: Mistral-7B for text, Stable Diffusion for images (configurable).

**Q: Can I use my own models?**
A: Yes, update model names in `config/agents_config.yaml`.

---

## 🎉 Examples

### Example 1: Adventure Story

```
Plot: A young explorer discovers a hidden world beneath their backyard
Themes: courage, curiosity, friendship
Age: 8-12
Length: Medium
Style: Children Book
```

### Example 2: Educational Story

```
Plot: A group of kids learn about recycling by helping clean up their neighborhood park
Themes: environment, teamwork, responsibility
Age: 5-7
Length: Short
Style: Cartoon
```

### Example 3: Fantasy Story

```
Plot: A shy bookworm finds a magical library where book characters come to life
Themes: imagination, confidence, adventure
Age: 10-14
Length: Long
Style: Watercolor
```

---

## 📝 Feedback and Contributions

We welcome feedback and contributions!

- Report issues on GitHub
- Suggest new features
- Share your generated stories
- Contribute code improvements

---

**Happy Story Creating! 📚✨**
