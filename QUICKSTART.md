# Quick Start Guide

## Installation

```bash
# Clone or download the project
cd AI-Story-Agents

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### 1. Simple Command Line

```bash
# Create a story from a plot idea
python main.py --plot "A brave mouse goes on an adventure to find cheese"

# Specify themes and age range
python main.py --plot "Your story idea" --themes friendship courage --age 8-12

# Choose art style
python main.py --plot "Your story" --art-style cartoon --length medium
```

### 2. Interactive Mode

```bash
python main.py --interactive
```

You'll be prompted to enter:
- Story plot/idea
- Themes
- Target age
- Story length
- Art style

### 3. Demo Mode

```bash
python main.py --demo
```

Runs a pre-configured example story.

### 4. Python API

```python
from orchestrator.coordinator import StoryOrchestrator

# Initialize
orchestrator = StoryOrchestrator()

# Create story
story_idea = {
    'plot': 'A shy kid discovers they can talk to animals',
    'target_age': '8-12',
    'themes': ['friendship', 'courage'],
    'length': 'short',
    'art_style': 'children_book'
}

result = orchestrator.create_story(story_idea)

# Access results
print(f"Created {result['metadata']['chapters']} chapters")
print(f"PDF: {result['publications']['pdf']}")
```

## Configuration

Edit `config/agents_config.yaml` to customize:

- **Models**: Change AI models for text and images
- **Art Style**: Adjust illustration style
- **Output Formats**: Choose PDF, HTML, EPUB
- **Performance**: Memory optimization, batch sizes

### Key Settings

```yaml
# Use smaller models for limited memory
author:
  model_name: "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
  load_in_8bit: true

illustrator:
  model_name: "runwayml/stable-diffusion-v1-5"
  num_inference_steps: 30  # Faster but lower quality
```

## Running on Google Colab

```python
# In Colab notebook
!git clone <your-repo-url>
%cd AI-Story-Agents

!pip install -r requirements.txt

# Run with GPU
!python main.py --plot "Your story idea" --config config/agents_config.yaml
```

## Output

Generated files are saved to `output/publications/`:
- `your_story.pdf` - Publication-ready PDF
- `your_story.html` - Web-ready HTML version
- `img_*.png` - Individual illustrations

## Examples

See `examples/` directory:
- `simple_story.py` - Basic usage
- `advanced_workflow.py` - Custom workflows and agent interactions

## Troubleshooting

### Out of Memory
- Enable 8-bit loading: `load_in_8bit: true`
- Use smaller models
- Run phases separately:
  ```bash
  python main.py --plot "..." --text-only
  python main.py --images-only
  python main.py --publish-only
  ```

### Slow Generation
- Reduce `num_inference_steps` (30 instead of 50)
- Use smaller image dimensions (512x512 instead of 768x1024)
- Use faster models (SD 1.5 instead of SDXL)

### Model Download Issues
- Models are downloaded from HuggingFace on first run
- Requires ~15GB disk space
- Use `cache_dir` in config to specify location

## Next Steps

1. Try the demo: `python main.py --demo`
2. Create your own story with custom plot
3. Experiment with different art styles
4. Customize agent behavior in config files
5. Explore agent communication in examples

## Support

- Check README.md for detailed documentation
- See examples/ for code samples
- Review config/agents_config.yaml for all options
