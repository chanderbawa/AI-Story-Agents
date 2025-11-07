"""
Simple Story Creation Example
Demonstrates basic usage of the AI Story Agents system.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.coordinator import StoryOrchestrator


def create_simple_story():
    """Create a simple story with minimal configuration."""
    
    print("🎬 Simple Story Creation Example")
    print("=" * 60)
    
    # Initialize orchestrator with default config
    orchestrator = StoryOrchestrator()
    
    # Define a simple story idea
    story_idea = {
        'plot': 'A curious cat discovers a magical garden where vegetables can talk',
        'target_age': '6-10',
        'themes': ['curiosity', 'friendship', 'nature'],
        'length': 'short',
        'art_style': 'children_book'
    }
    
    print(f"\n📖 Creating story: {story_idea['plot']}")
    print(f"🎯 Target age: {story_idea['target_age']}")
    print(f"🎨 Themes: {', '.join(story_idea['themes'])}")
    
    # Create the story
    result = orchestrator.create_story(story_idea)
    
    if result['status'] == 'complete':
        print("\n✅ Story created successfully!")
        print(f"\n📊 Results:")
        print(f"   Chapters: {result['metadata']['chapters']}")
        print(f"   Images: {result['metadata']['images']}")
        print(f"   Pages: {result['metadata']['page_count']}")
        
        print(f"\n📁 Files created:")
        for format_type, filepath in result['publications'].items():
            print(f"   {format_type.upper()}: {filepath}")
    else:
        print("\n❌ Story creation failed")
    
    return result


if __name__ == '__main__':
    create_simple_story()
