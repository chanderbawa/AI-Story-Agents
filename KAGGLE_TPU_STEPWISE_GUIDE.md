# Kaggle TPU - Step-by-Step Story Generation Guide

## 🎯 Overview

This approach lets you **review each agent's output** before proceeding to the next step. This way you can catch quality issues early and regenerate if needed.

## 📋 Prerequisites

1. **Enable TPU in Kaggle:**
   - Right sidebar → Accelerator → **TPU v3-8**
   - You have 20 hours/week of TPU time

2. **Enable Internet:**
   - Settings → Internet → **ON**

## 🚀 Step-by-Step Process

### STEP 1: Generate Story Text

**File:** `kaggle_tpu_stepwise.py`

**What it does:**
- Loads only the Author Agent
- Generates story text based on your plot
- Shows you all chapters
- **STOPS** for your review

**How to use:**
1. Copy the entire `kaggle_tpu_stepwise.py` into a Kaggle cell
2. Customize the `story_idea` section with your plot
3. Run the cell
4. **Review the generated story text**
5. If good → proceed to Step 2
6. If bad → modify settings and re-run

**What to check:**
- ✅ Does the story follow your plot?
- ✅ Is the language age-appropriate?
- ✅ Are the characters correct?
- ✅ Is it engaging for kids?

---

### STEP 2: Generate Illustrations

**File:** `kaggle_tpu_step2_illustrations.py`

**What it does:**
- Loads the story from Step 1
- Loads only the Illustrator Agent
- Generates cartoon-style images
- Shows you preview images
- **STOPS** for your review

**How to use:**
1. Copy `kaggle_tpu_step2_illustrations.py` into a **NEW** cell
2. Run the cell
3. **Review the generated illustrations**
4. If good → proceed to Step 3
5. If bad → adjust settings and re-run

**What to check:**
- ✅ Are images cartoon-style and kid-friendly?
- ✅ Do they match the story scenes?
- ✅ Are characters recognizable?
- ✅ Is the quality good enough?

---

### STEP 3: Create PDF and HTML

**File:** `kaggle_tpu_step3_publish.py`

**What it does:**
- Loads story + illustrations from previous steps
- Loads only the Publisher Agent
- Creates PDF and HTML files
- Provides download links

**How to use:**
1. Copy `kaggle_tpu_step3_publish.py` into a **NEW** cell
2. Run the cell
3. Download your files!

**Output:**
- `kids_story.pdf` - Print-ready PDF
- `kids_story.html` - Web preview
- `kids_story.zip` - Both files

---

## 🔧 Customization Options

### Improve Story Quality

If the story text is poor, modify these settings in Step 1:

```python
# In kaggle_tpu_stepwise.py, find this section:

config['author']['temperature'] = 0.7  # Try 0.8 or 0.9 for more creativity
config['author']['top_p'] = 0.9        # Try 0.95 for more variety
config['author']['max_length'] = 500   # Increase to 800 for longer chapters
```

### Better Model for Story Text

Replace TinyLlama with a better model (requires more memory):

```python
# WARNING: May cause out-of-memory errors
config['author']['model_name'] = 'microsoft/phi-2'  # Better but larger
```

### Improve Illustration Quality

Modify these settings in Step 2:

```python
# In kaggle_tpu_step2_illustrations.py:

config['illustrator']['width'] = 768              # Higher resolution
config['illustrator']['height'] = 768
config['illustrator']['num_inference_steps'] = 30 # More steps = better quality
config['illustrator']['guidance_scale'] = 9.0     # Stronger prompt following
```

### Change Art Style

```python
# In your story_idea:
'art_style': 'cartoon'        # Options: cartoon, watercolor, children_book, line_art
```

---

## 🐛 Troubleshooting

### Problem: Story text is gibberish or instructions

**Cause:** TinyLlama is too weak for creative writing

**Solution:** Provide a **very detailed plot** with actual dialogue:

```python
story_idea = {
    'plot': '''
    CHAPTER 1: The New School
    
    Leo walked into the classroom. "Wow, so many kids!" he thought.
    The teacher smiled. "Welcome, Leo! Find a seat."
    
    CHAPTER 2: The Friendship Bench
    
    At recess, Leo saw a boy sitting alone.
    "Hi! I'm Leo. What's your name?" Leo asked.
    "I'm Finn," the boy said quietly.
    "Want to play tag?" Leo asked with a big smile.
    Finn's face lit up. "Yes!"
    
    CHAPTER 3: Best Friends
    
    They ran and played. They laughed together.
    "You're my best friend!" said Finn.
    "You're my best friend too!" said Leo.
    They were both very happy.
    ''',
    # ... rest of config
}
```

### Problem: Images don't match the story

**Cause:** Image prompts are auto-generated and may be off

**Solution:** In Step 2, you can manually edit the scene descriptions before generating images.

### Problem: Out of memory error

**Cause:** Models too large for available memory

**Solution:**
1. Use CPU for text generation (already configured)
2. Reduce image size to 512x512
3. Use fewer inference steps (15 instead of 20)

### Problem: TPU not being used

**Note:** TPUs are optimized for parallel training, not sequential text generation. For this use case:
- Text generation: **CPU is fine** (autoregressive, can't parallelize)
- Image generation: **GPU is better** than TPU for Stable Diffusion

**Recommendation:** Use **GPU T4** instead of TPU for this workload.

---

## 📊 Expected Timeline

| Step | Task | Time |
|------|------|------|
| 1 | Story Text | 2-3 min |
| 2 | Illustrations (6 images) | 3-5 min |
| 3 | PDF/HTML | 30 sec |
| **Total** | | **6-9 min** |

---

## ✅ Best Practices

1. **Start simple:** Use a very simple plot first to test the system
2. **Review each step:** Don't skip the review phases
3. **Iterate:** If output is bad, adjust settings and re-run that step only
4. **Save your work:** The system saves intermediate files so you don't lose progress
5. **Use detailed plots:** The more detail you provide, the better the output

---

## 🎨 Example: High-Quality Story Idea

```python
story_idea = {
    'plot': '''
    SETTING: Sunshine Elementary School, a bright and colorful school with a big playground.
    
    CHARACTERS:
    - Leo: A 9-year-old boy with curly brown hair, wearing a blue t-shirt. He's friendly and brave.
    - Finn: A 9-year-old boy with red hair and freckles, wearing a green shirt. He's shy but kind.
    
    CHAPTER 1: The First Day
    Leo walks into his new classroom. He sees colorful posters on the walls.
    "Good morning, Leo!" says Ms. Johnson, his teacher.
    Leo waves and finds a desk by the window.
    
    CHAPTER 2: The Friendship Bench
    At recess, Leo sees a yellow bench. A sign says "Friendship Bench."
    A boy with red hair sits there alone, looking sad.
    Leo takes a deep breath. "I can do this," he thinks.
    He walks over. "Hi! I'm Leo. Want to play?"
    The boy looks up. "I'm Finn. I'd love to!"
    
    CHAPTER 3: Best Friends Forever
    Leo and Finn play tag. They laugh and run.
    They share cookies at snack time.
    "You're really nice, Leo," says Finn.
    "You're nice too, Finn! Let's be best friends!" says Leo.
    They high-five and smile.
    From that day on, they were best friends.
    
    THE END.
    ''',
    'target_age': '6-8',
    'themes': ['friendship', 'kindness', 'bravery'],
    'length': 'short',
    'art_style': 'cartoon'
}
```

---

## 🚀 Quick Start

**In Kaggle:**

1. Enable TPU or GPU
2. Enable Internet
3. Create 3 cells
4. Paste each step's code into a separate cell
5. Run Cell 1 → Review → Run Cell 2 → Review → Run Cell 3
6. Download your story!

---

## 💡 Pro Tips

1. **For better story quality:** Write the entire story yourself in the plot field, let the AI just format it
2. **For better images:** Use very specific scene descriptions with character details
3. **For faster generation:** Use 512x512 images with 15 steps
4. **For higher quality:** Use 768x768 images with 30 steps (slower)

---

## 📝 Summary

This step-by-step approach gives you **full control** over the story generation process. You can:
- ✅ Review each agent's output
- ✅ Regenerate individual steps
- ✅ Adjust settings between steps
- ✅ Catch quality issues early
- ✅ Save time by not regenerating everything

Good luck creating amazing kids' stories! 🎉📚
