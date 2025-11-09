"""
Kaggle TPU - STEP 2: Generate Illustrations
Run this AFTER reviewing the story text
"""

import os
import pickle

print("="*70)
print("🎨 STEP 2: GENERATING ILLUSTRATIONS")
print("="*70)

# Load story data from previous step
print("\n📂 Loading story data...")
with open('/kaggle/working/story_data.pkl', 'rb') as f:
    story_data = pickle.load(f)

chapters = story_data.get('chapters', [])
print(f"✅ Loaded {len(chapters)} chapters")

# ============================================
# LOAD ILLUSTRATOR AGENT
# ============================================

print("\n📥 Loading Illustrator Agent...")

os.chdir('/kaggle/working/AI-Story-Agents')

import yaml
with open('config/agents_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

from agents.illustrator_agent import IllustratorAgent

illustrator = IllustratorAgent(config.get('illustrator', {}))
print("✅ Illustrator Agent loaded")

# ============================================
# GENERATE ILLUSTRATIONS
# ============================================

print("\n" + "="*70)
print("🎨 GENERATING ILLUSTRATIONS")
print("="*70)

from agents.base_agent import Message

# Prepare illustration request
scenes_for_illustration = story_data.get('scenes_for_illustration', [])

print(f"📸 Generating {len(scenes_for_illustration)} illustrations...")
print("⏳ This will take 3-5 minutes (20-30 sec per image)")

request = Message(
    sender='User',
    recipient='IllustratorAgent',
    message_type='request',
    content={
        'action': 'create_illustrations',
        'story': story_data,
        'art_style': 'cartoon',
        'target_age': '6-8'
    }
)

response = illustrator.process_message(request)

# Display results
print("\n" + "="*70)
print("🖼️  ILLUSTRATIONS GENERATED")
print("="*70)

if response and response.content.get('status') == 'complete':
    illustrations = response.content.get('illustrations', [])
    
    print(f"✅ Generated {len(illustrations)} illustrations")
    
    # Show each illustration info
    for i, ill in enumerate(illustrations, 1):
        print(f"\n{i}. {ill.get('scene_id', 'Unknown')}")
        print(f"   File: {ill.get('image_path', 'N/A')}")
        print(f"   Caption: {ill.get('caption', 'N/A')[:80]}...")
    
    # Save illustration data
    story_data['illustrations'] = illustrations
    with open('/kaggle/working/story_with_images.pkl', 'wb') as f:
        pickle.dump(story_data, f)
    
    print("\n✅ Story with illustrations saved")
    
    # Display sample images
    from IPython.display import Image, display
    
    print("\n" + "="*70)
    print("📸 PREVIEW ILLUSTRATIONS")
    print("="*70)
    
    for ill in illustrations[:3]:  # Show first 3
        img_path = ill.get('image_path')
        if img_path and os.path.exists(img_path):
            print(f"\n{ill.get('caption', 'Illustration')}")
            display(Image(filename=img_path, width=400))
    
    print("\n" + "="*70)
    print("⚠️  REVIEW THE ILLUSTRATIONS ABOVE")
    print("="*70)
    print("Do the illustrations look good?")
    print("- If YES: Run NEXT cell to create PDF/HTML")
    print("- If NO: Stop and adjust illustration settings")
    print("="*70)
    
else:
    print("❌ Illustration generation failed!")
    print(f"Status: {response.content.get('status') if response else 'No response'}")

print("\n🛑 STOP HERE - REVIEW THE ILLUSTRATIONS")
