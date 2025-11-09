"""
Kaggle TPU - STEP 3: Create PDF and HTML
Run this AFTER reviewing illustrations
"""

import os
import pickle

print("="*70)
print("📚 STEP 3: CREATING PDF AND HTML")
print("="*70)

# Load story with illustrations
print("\n📂 Loading story with illustrations...")
with open('/kaggle/working/story_with_images.pkl', 'rb') as f:
    story_data = pickle.load(f)

print(f"✅ Loaded story with {len(story_data.get('chapters', []))} chapters")
print(f"✅ Loaded {len(story_data.get('illustrations', []))} illustrations")

# ============================================
# LOAD PUBLISHER AGENT
# ============================================

print("\n📥 Loading Publisher Agent...")

os.chdir('/kaggle/working/AI-Story-Agents')

import yaml
with open('config/agents_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

from agents.publisher_agent import PublisherAgent

publisher = PublisherAgent(config.get('publisher', {}))
print("✅ Publisher Agent loaded")

# ============================================
# CREATE PUBLICATIONS
# ============================================

print("\n" + "="*70)
print("📚 CREATING PDF AND HTML")
print("="*70)

from agents.base_agent import Message

request = Message(
    sender='User',
    recipient='PublisherAgent',
    message_type='request',
    content={
        'action': 'create_publication',
        'story': story_data,
        'formats': ['pdf', 'html']
    }
)

print("⏳ Creating publications...")
response = publisher.process_message(request)

# Display results
print("\n" + "="*70)
print("✅ PUBLICATIONS CREATED")
print("="*70)

if response and response.content.get('status') == 'complete':
    publications = response.content.get('publications', {})
    
    print("\n📁 Output Files:")
    for format_type, filepath in publications.items():
        print(f"   {format_type.upper()}: {filepath}")
    
    # Copy to /kaggle/working for easy download
    import shutil
    import zipfile
    
    pdf_dest = '/kaggle/working/kids_story.pdf'
    html_dest = '/kaggle/working/kids_story.html'
    zip_path = '/kaggle/working/kids_story.zip'
    
    if 'pdf' in publications:
        shutil.copy2(publications['pdf'], pdf_dest)
        print(f"\n✅ PDF copied to: {pdf_dest}")
    
    if 'html' in publications:
        shutil.copy2(publications['html'], html_dest)
        print(f"✅ HTML copied to: {html_dest}")
    
    # Create zip
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        if os.path.exists(pdf_dest):
            zipf.write(pdf_dest, 'kids_story.pdf')
        if os.path.exists(html_dest):
            zipf.write(html_dest, 'kids_story.html')
    
    print(f"✅ ZIP created: {zip_path}")
    
    # Download links
    from IPython.display import FileLink, display
    
    print("\n" + "="*70)
    print("📥 DOWNLOAD YOUR STORY")
    print("="*70)
    
    print("\n📦 ZIP File (both PDF and HTML):")
    display(FileLink(zip_path))
    
    print("\n📄 PDF File:")
    display(FileLink(pdf_dest))
    
    print("\n🌐 HTML File:")
    display(FileLink(html_dest))
    
    print("\n" + "="*70)
    print("🎉 STORY COMPLETE!")
    print("="*70)
    print("Right-click the links above and select 'Save As' to download")
    
else:
    print("❌ Publication failed!")
    print(f"Status: {response.content.get('status') if response else 'No response'}")

print("\n✨ DONE!")
