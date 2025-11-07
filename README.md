# AI Story Creation Agents

A multi-agent AI system for collaborative story creation, featuring specialized agents that work together to create illustrated children's books from simple story ideas.

## 🤖 Agent Architecture

### **Author Agent** (Middle School Writer)
- Takes story plots/ideas as input
- Develops characters, dialogue, and narrative arcs
- Writes age-appropriate content with engaging voice
- Collaborates with illustrator for scene descriptions
- Maintains story consistency and pacing

### **Illustrator Agent** (Visual Artist)
- Interprets story scenes and creates visual descriptions
- Generates images that support the narrative
- Maintains consistent character appearance across illustrations
- Adapts art style based on target audience
- Provides feedback to author about visual storytelling

### **Publisher Agent** (Production Manager)
- Coordinates the workflow between agents
- Assembles text and images into professional layouts
- Generates publication-ready PDFs
- Handles formatting, typography, and design
- Exports in multiple formats (print, digital, web)

## 🎯 Key Features

- **Agent Communication**: Agents exchange messages and collaborate on creative decisions
- **Iterative Refinement**: Agents can request revisions from each other
- **Style Consistency**: Maintains consistent tone, voice, and visual style
- **Flexible Input**: Works with simple plot ideas, detailed outlines, or character descriptions
- **Multiple Formats**: Outputs to PDF, EPUB, web-ready HTML
- **Quality Control**: Built-in review and approval workflows

## 🚀 Quick Start

### 🌐 Web Interface (Recommended)

Launch the user-friendly web interface:

**With GPU:**
```bash
pip install -r requirements.txt
python app.py
```

**Without GPU (CPU only):**
```bash
pip install -r requirements.txt
python app_cpu.py  # Optimized for CPU
```

Then open your browser to `http://localhost:7860` and start creating stories!

**Guides:**
- **CPU Mode:** See [CPU_SETUP.md](CPU_SETUP.md) or [QUICK_START_CPU.md](QUICK_START_CPU.md)
- **Google Colab (Free GPU):** See [COLAB_SETUP.md](COLAB_SETUP.md)

### 💻 Command Line Interface

```bash
# Create a story from a simple idea
python main.py --plot "A shy kid discovers they can talk to animals"

# Interactive mode
python main.py --interactive

# Run demo
python main.py --demo
```

### 🐍 Python API

```python
from orchestrator.coordinator import StoryOrchestrator

# Initialize the multi-agent system
orchestrator = StoryOrchestrator()

# Provide a story idea
story_idea = {
    "plot": "A shy kid discovers they can talk to animals and helps save the school garden",
    "target_age": "8-12",
    "themes": ["friendship", "courage", "nature"],
    "length": "short"
}

# Let the agents collaborate
result = orchestrator.create_story(story_idea)

# Access the PDF
print(f"PDF saved to: {result['publications']['pdf']}")
```

## 📁 Project Structure

```
AI-Story-Agents/
├── agents/
│   ├── base_agent.py          # Base agent class
│   ├── author_agent.py        # Story writing agent
│   ├── illustrator_agent.py   # Image generation agent
│   └── publisher_agent.py     # PDF assembly agent
├── orchestrator/
│   ├── coordinator.py         # Agent coordination
│   └── __init__.py
├── config/
│   └── agents_config.yaml     # Agent configurations
├── examples/
│   ├── simple_story.py        # Basic usage
│   └── advanced_workflow.py   # Custom workflows
├── main.py                    # CLI interface
├── app.py                     # Web interface launcher
├── web_interface.py           # Gradio web interface
├── COLAB_SETUP.md            # Google Colab guide
├── QUICKSTART.md             # Quick start guide
└── requirements.txt           # Dependencies
```

## 🎨 Agent Collaboration Example

```
User Input: "A plump kid uses kindness to make friends"

Author Agent → "I'll develop Leo, a witty 9-year-old who uses humor..."
              ↓
Illustrator Agent → "I need character descriptions for Leo..."
              ↓
Author Agent → "Leo is plump with expressive eyes, always smiling..."
              ↓
Illustrator Agent → "Generated character sheet. Proceeding with scene 1..."
              ↓
Publisher Agent → "Received Chapter 1 text and 3 images. Assembling..."
              ↓
Final Output: Complete illustrated book PDF
```

## 🌐 Web Interface Features

The Gradio-based web interface provides:

- **User-Friendly Form**: Easy input for story ideas, themes, and preferences
- **Real-Time Progress**: Live updates during story generation
- **PDF Download**: Direct download of generated illustrated books
- **Preview Panel**: View story statistics and metadata
- **Demo Mode**: Quick test with pre-configured example story
- **Mobile Responsive**: Works on desktop, tablet, and mobile devices
- **Public Sharing**: Create shareable links (perfect for Colab)

## 🛠️ Advanced Features

- **Agent Memory**: Agents remember previous interactions and maintain context
- **Style Transfer**: Apply different writing and art styles
- **Multi-language**: Generate stories in multiple languages
- **Interactive Mode**: Real-time collaboration with human feedback
- **Batch Processing**: Create multiple story variations
- **Quality Metrics**: Automated story quality assessment

## 📋 Requirements

- Python 3.11+
- PyTorch 2.0+
- Transformers 4.35+
- Diffusers 0.24+
- ReportLab 4.0+
- Gradio 4.0+ (for web interface)
- GPU recommended (or Google Colab with T4 GPU)

## 🎓 Use Cases

1. **Educational Content**: Generate custom stories for specific learning objectives
2. **Personalized Books**: Create stories featuring the reader as a character
3. **Rapid Prototyping**: Quickly test story concepts and illustrations
4. **Content Creation**: Generate multiple story variations for A/B testing
5. **Accessibility**: Create stories in multiple formats and languages

## 🔮 Future Enhancements

- **Editor Agent**: Reviews and suggests improvements
- **Voice Agent**: Adds narration and character voices
- **Animation Agent**: Creates simple animations from illustrations
- **Marketing Agent**: Generates promotional materials
- **Translation Agent**: Adapts stories for different cultures

## 📄 License

MIT License - Feel free to use and modify for your projects!
