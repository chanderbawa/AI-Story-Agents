# 🚀 Kaggle Quick Start - AI Story Generator

## The Problem You Encountered

**TinyLlama generates garbage** - it outputs writing instructions instead of actual stories because it's not instruction-tuned.

## ✅ The Solution

Use **Llama 3.2 1B** - Meta's latest small model that actually follows instructions!

---

## 📝 Step-by-Step Setup

### 1. Get Hugging Face Token (30 seconds)

1. Go to: https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Name: `kaggle-stories`
4. Type: **Read**
5. Click **"Generate"**
6. **Copy the token** (starts with `hf_...`)

### 2. Create Kaggle Notebook

1. Go to https://www.kaggle.com
2. Click **Code** → **New Notebook**
3. Settings (right sidebar):
   - **Accelerator:** GPU T4 x2
   - **Internet:** ON

### 3. Add Token (Cell 1)

```python
# ============================================
# CELL 1: SETUP AND AUTHENTICATION
# ============================================

import os
from huggingface_hub import login

# Replace with your token from step 1
os.environ['HF_TOKEN'] = 'hf_your_token_here'  # ← PASTE YOUR TOKEN

login(token=os.environ['HF_TOKEN'])

print("✅ Authenticated with Hugging Face")
```

### 4. Generate Story (Cell 2)

```python
# ============================================
# CELL 2: GENERATE STORY WITH LLAMA 3.2
# ============================================

import os
import sys

# Setup
os.chdir('/kaggle/working')
if not os.path.exists('AI-Story-Agents'):
    get_ipython().system('git clone https://github.com/chanderbawa/AI-Story-Agents.git')
os.chdir('/kaggle/working/AI-Story-Agents')
get_ipython().system('pip install -q -r requirements.txt')

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class StoryWriter:
    def __init__(self):
        print("📥 Loading Llama 3.2 1B...")
        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
        self.model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-3.2-1B-Instruct",
            device_map="cuda",
            torch_dtype=torch.float16
        )
        print("✅ Model loaded!")
    
    def generate_chapter(self, chapter_num, plot):
        messages = [
            {"role": "system", "content": "You are a children's book author. Write engaging stories for ages 6-8 with simple language, dialogue, and emotion."},
            {"role": "user", "content": f"Write Chapter {chapter_num} of this story:\n\n{plot}\n\nMake it 150-200 words with dialogue and descriptions."}
        ]
        
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=400,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.split("assistant")[-1].strip()
    
    def create_story(self, plot):
        chapters = []
        for i in range(1, 4):
            print(f"\n✍️  Writing Chapter {i}...")
            text = self.generate_chapter(i, plot)
            chapters.append({'number': i, 'title': f'Chapter {i}', 'text': text})
            print(f"✅ Done ({len(text)} chars)")
        return chapters

# YOUR STORY PLOT - CUSTOMIZE THIS!
plot = """
Leo is a 9-year-old boy starting at Sunshine Elementary School.

On his first day, he walks into a bright classroom. His teacher Ms. Johnson welcomes him warmly.

At recess, Leo sees a boy named Finn sitting alone on a yellow bench. Finn looks sad.

Leo walks over and says "Hi! I'm Leo. Want to play?"

Finn smiles big. "Yes! I'm Finn!"

They play tag, laugh, and share snacks under a tree.

"You're my best friend!" says Finn.
"You're my best friend too!" says Leo.

Leo learns that being brave and kind makes wonderful friendships.
"""

# Generate
writer = StoryWriter()
chapters = writer.create_story(plot)

# Display
print("\n" + "="*70)
print("📚 YOUR STORY")
print("="*70)

for ch in chapters:
    print(f"\n{'='*70}")
    print(f"CHAPTER {ch['number']}")
    print(f"{'='*70}")
    print(ch['text'])

# Save
import pickle
with open('/kaggle/working/story_data.pkl', 'wb') as f:
    pickle.dump({'chapters': chapters}, f)

print("\n✅ Story saved! Review above, then run Cell 3 for illustrations.")
```

### 5. Generate Illustrations (Cell 3)

```python
# ============================================
# CELL 3: GENERATE ILLUSTRATIONS
# ============================================

import os
import pickle
from diffusers import StableDiffusionPipeline
import torch

# Load story
with open('/kaggle/working/story_data.pkl', 'rb') as f:
    story_data = pickle.load(f)

print(f"📖 Loaded {len(story_data['chapters'])} chapters")

# Load Stable Diffusion
print("\n📥 Loading Stable Diffusion...")
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

print("✅ Ready to generate images")

# Generate images
scenes = [
    "A friendly boy named Leo walking into a bright, colorful elementary school classroom, children's book illustration, cartoon style",
    "A sad boy with red hair sitting alone on a yellow bench at a playground, children's book illustration, cartoon style",
    "Two happy boys playing tag and laughing on a sunny playground, children's book illustration, cartoon style"
]

images = []
for i, prompt in enumerate(scenes, 1):
    print(f"\n🎨 Generating image {i}/3...")
    image = pipe(prompt, num_inference_steps=20, guidance_scale=8.0).images[0]
    path = f'/kaggle/working/image_{i}.png'
    image.save(path)
    images.append(path)
    print(f"✅ Saved: {path}")

# Display
from IPython.display import Image, display

print("\n" + "="*70)
print("🖼️  YOUR ILLUSTRATIONS")
print("="*70)

for path in images:
    display(Image(filename=path, width=400))

print("\n✅ All done! Run Cell 4 to create PDF.")
```

### 6. Create PDF (Cell 4)

```python
# ============================================
# CELL 4: CREATE PDF
# ============================================

import pickle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# Load story
with open('/kaggle/working/story_data.pkl', 'rb') as f:
    story_data = pickle.load(f)

# Create PDF
pdf_path = '/kaggle/working/kids_story.pdf'
doc = SimpleDocTemplate(pdf_path, pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Title
story.append(Paragraph("Leo's New Friend", styles['Title']))
story.append(Spacer(1, 0.5*inch))

# Chapters with images
for i, chapter in enumerate(story_data['chapters'], 1):
    # Chapter title
    story.append(Paragraph(f"Chapter {i}", styles['Heading1']))
    story.append(Spacer(1, 0.2*inch))
    
    # Chapter text
    story.append(Paragraph(chapter['text'], styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Image
    img_path = f'/kaggle/working/image_{i}.png'
    img = RLImage(img_path, width=4*inch, height=4*inch)
    story.append(img)
    story.append(Spacer(1, 0.5*inch))

doc.build(story)

# Download
from IPython.display import FileLink, display

print("="*70)
print("🎉 STORY COMPLETE!")
print("="*70)
print("\n📥 DOWNLOAD YOUR BOOK:")
display(FileLink(pdf_path))

print("\n✅ Right-click and select 'Save As' to download!")
```

---

## 🎯 That's It!

Run the 4 cells in order:
1. **Cell 1:** Authenticate
2. **Cell 2:** Generate story text (2-3 min)
3. **Cell 3:** Generate illustrations (2-3 min)
4. **Cell 4:** Create PDF (10 sec)

**Total time: ~5-7 minutes**

---

## 💡 Customize Your Story

In Cell 2, edit the `plot` variable:

```python
plot = """
YOUR STORY HERE!

Include:
- Character names and ages
- Setting details
- What happens in each part
- Dialogue you want
- The lesson/message
"""
```

The AI will follow your plot and create an engaging story!

---

## 🆘 Troubleshooting

### "Token is invalid"
- Get a new token from https://huggingface.co/settings/tokens
- Make sure it has **Read** access

### "Out of memory"
- Restart kernel
- Use GPU T4 x2 (not TPU)

### "Story is still bad"
- Make your plot MORE detailed
- Include specific dialogue
- Describe scenes clearly
- Add character emotions

---

## 🎉 Success!

You now have an **autonomous AI agent** that:
- ✅ Takes your plot
- ✅ Generates engaging story text
- ✅ Creates cartoon illustrations
- ✅ Produces a downloadable PDF

**Share your stories!** 📚✨
