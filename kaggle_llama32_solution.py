"""
Kaggle - Using Llama 3.2 1B for Story Generation
Llama 3.2 is Meta's latest small model - much better than TinyLlama
"""

import os
import sys

print("="*70)
print("🦙 AI STORY GENERATOR - LLAMA 3.2")
print("="*70)

# Setup
os.chdir('/kaggle/working')
if not os.path.exists('AI-Story-Agents'):
    get_ipython().system('git clone https://github.com/chanderbawa/AI-Story-Agents.git')
os.chdir('/kaggle/working/AI-Story-Agents')

get_ipython().system('pip install -q -r requirements.txt')

# ============================================
# Use Llama 3.2 1B - Much better than TinyLlama
# ============================================

print("\n⚙️  Using Llama 3.2 1B (Meta's latest small model)")

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class Llama32StoryWriter:
    """Story writer using Llama 3.2 1B."""
    
    def __init__(self):
        self.model_name = "meta-llama/Llama-3.2-1B-Instruct"
        
        print(f"\n📥 Loading {self.model_name}...")
        print("   This may take 1-2 minutes...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="cuda",
            torch_dtype=torch.float16  # Use FP16 for speed
        )
        
        print("✅ Llama 3.2 loaded!")
    
    def generate_chapter(self, chapter_num, plot, previous_chapters=""):
        """Generate one chapter using Llama 3.2."""
        
        # Use Llama's chat format
        messages = [
            {
                "role": "system",
                "content": "You are a children's book author writing engaging stories for ages 6-8. Write in simple, clear language with dialogue and emotion."
            },
            {
                "role": "user",
                "content": f"""Write Chapter {chapter_num} of a children's story.

Plot Summary:
{plot}

{f"Previous chapters: {previous_chapters}" if previous_chapters else ""}

Write Chapter {chapter_num} with:
- Simple sentences for young readers
- Dialogue between characters
- Descriptions of what characters see and feel
- An engaging scene
- 150-200 words

Chapter {chapter_num}:"""
            }
        ]
        
        # Format for Llama
        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=400,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the chapter text (after the prompt)
        chapter_text = response.split("Chapter " + str(chapter_num) + ":")[-1].strip()
        
        return chapter_text
    
    def create_story(self, story_idea):
        """Create complete story."""
        plot = story_idea['plot']
        
        print("\n📝 Generating story with Llama 3.2...")
        
        chapters = []
        previous_text = ""
        
        for i in range(1, 4):
            print(f"\n✍️  Writing Chapter {i}...")
            
            chapter_text = self.generate_chapter(i, plot, previous_text)
            
            chapters.append({
                'number': i,
                'title': f'Chapter {i}',
                'text': chapter_text
            })
            
            previous_text += f"\nChapter {i}: {chapter_text[:100]}..."
            
            print(f"✅ Chapter {i} complete")
        
        # Create illustration scenes
        scenes = [
            {
                'id': f'scene_ch{i}_1',
                'chapter': i,
                'description': f'Key scene from chapter {i}',
                'characters': ['Leo', 'Finn'],
                'mood': 'happy',
                'setting': 'school'
            }
            for i in range(1, 4)
        ]
        
        return {
            'chapters': chapters,
            'plot': plot,
            'themes': story_idea.get('themes', []),
            'target_age': story_idea.get('target_age', '6-8'),
            'characters': [
                {'name': 'Leo', 'personality': 'friendly, brave'},
                {'name': 'Finn', 'personality': 'shy, kind'}
            ],
            'scenes_for_illustration': scenes
        }

# ============================================
# Initialize and Generate
# ============================================

writer = Llama32StoryWriter()

print("\n" + "="*70)
print("📖 CREATING STORY")
print("="*70)

story_idea = {
    'plot': '''
    Leo is a 9-year-old boy starting at Sunshine Elementary School.
    
    On his first day, he walks into a bright classroom. His teacher Ms. Johnson welcomes him with a warm smile.
    
    At recess, Leo sees a boy named Finn sitting alone on a yellow bench called the Friendship Bench. Finn looks sad because he's new and has no friends.
    
    Leo takes a deep breath and walks over. "Hi! I'm Leo. Want to play?" he asks.
    
    Finn's face lights up. "Yes! I'm Finn!" he says happily.
    
    They play tag on the playground, laughing and running together. They share snacks under a big tree.
    
    "You're my best friend!" says Finn.
    "You're my best friend too!" says Leo.
    
    Leo learns that being brave and kind is the best way to make friends.
    ''',
    'target_age': '6-8',
    'themes': ['friendship', 'kindness', 'bravery'],
    'length': 'short'
}

story_data = writer.create_story(story_idea)

# Display
print("\n" + "="*70)
print("📚 STORY COMPLETE")
print("="*70)

for chapter in story_data['chapters']:
    print(f"\n{'='*70}")
    print(f"CHAPTER {chapter['number']}: {chapter['title']}")
    print(f"{'='*70}")
    print(chapter['text'])
    print()

# Save
import pickle
with open('/kaggle/working/story_data.pkl', 'wb') as f:
    pickle.dump(story_data, f)

print("\n" + "="*70)
print("🛑 REVIEW THE STORY")
print("="*70)
print("Does the story follow the plot and make sense?")
print("\n✅ If YES → Run Cell 2 for illustrations")
print("❌ If NO → Adjust settings and re-run")
