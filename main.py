#!/usr/bin/env python3
"""
AI Story Agents - Main Entry Point
Create illustrated children's books using collaborative AI agents.
"""

import argparse
import yaml
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from orchestrator.coordinator import StoryOrchestrator


def load_config(config_path: str = None):
    """Load configuration from YAML file."""
    
    if config_path and Path(config_path).exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    return None


def main():
    parser = argparse.ArgumentParser(
        description='AI Story Agents - Collaborative Story Creation System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a story from a simple idea
  python main.py --plot "A shy kid discovers they can talk to animals"
  
  # Use a configuration file
  python main.py --config story_config.yaml
  
  # Interactive mode
  python main.py --interactive
  
  # Specify output directory
  python main.py --plot "Adventure story" --output ./my_stories
        """
    )
    
    parser.add_argument(
        '--plot',
        type=str,
        help='Story plot or idea'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration YAML file'
    )
    
    parser.add_argument(
        '--themes',
        nargs='+',
        default=['friendship', 'courage'],
        help='Story themes (e.g., friendship courage adventure)'
    )
    
    parser.add_argument(
        '--age',
        type=str,
        default='8-12',
        help='Target age range (default: 8-12)'
    )
    
    parser.add_argument(
        '--length',
        choices=['short', 'medium', 'long'],
        default='short',
        help='Story length (default: short)'
    )
    
    parser.add_argument(
        '--art-style',
        type=str,
        default='children_book',
        choices=['children_book', 'cartoon', 'watercolor', 'line_art'],
        help='Illustration art style'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='output/publications',
        help='Output directory for generated files'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run demo with example story'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    if config:
        print(f"📋 Loaded configuration from {args.config}")
    
    # Initialize orchestrator
    print("\n🎬 Initializing AI Story Agents...")
    orchestrator = StoryOrchestrator(config)
    
    # Determine story idea
    if args.demo:
        story_idea = get_demo_story()
        print("\n📖 Running demo story...")
    elif args.interactive:
        story_idea = interactive_mode()
    elif args.plot:
        story_idea = {
            'plot': args.plot,
            'target_age': args.age,
            'themes': args.themes,
            'length': args.length,
            'art_style': args.art_style
        }
    else:
        parser.print_help()
        return
    
    # Update output directory
    if config:
        config['output_dir'] = args.output
    
    # Create the story
    print("\n" + "=" * 70)
    print("🚀 STARTING STORY CREATION")
    print("=" * 70)
    
    result = orchestrator.create_story(story_idea)
    
    if result['status'] == 'complete':
        print("\n" + "=" * 70)
        print("✅ SUCCESS! Your story is ready!")
        print("=" * 70)
        print(f"\n📊 Story Statistics:")
        print(f"   Chapters: {result['metadata']['chapters']}")
        print(f"   Illustrations: {result['metadata']['images']}")
        print(f"   Pages: {result['metadata']['page_count']}")
        
        print(f"\n📁 Output Files:")
        for format_type, filepath in result['publications'].items():
            print(f"   {format_type.upper()}: {filepath}")
        
        print("\n🎉 Your illustrated story book is complete!")
        
    else:
        print("\n❌ Story creation failed. Please check the logs.")


def interactive_mode():
    """Interactive mode for story creation."""
    
    print("\n" + "=" * 70)
    print("🎨 INTERACTIVE STORY CREATION")
    print("=" * 70)
    
    plot = input("\n📝 Enter your story plot or idea:\n> ")
    
    print("\n🎯 Enter themes (comma-separated, e.g., friendship, courage, adventure):")
    themes_input = input("> ")
    themes = [t.strip() for t in themes_input.split(',')]
    
    print("\n👶 Target age range (e.g., 8-12):")
    age = input("> ") or "8-12"
    
    print("\n📏 Story length (short/medium/long):")
    length = input("> ") or "short"
    
    print("\n🎨 Art style (children_book/cartoon/watercolor/line_art):")
    art_style = input("> ") or "children_book"
    
    return {
        'plot': plot,
        'target_age': age,
        'themes': themes,
        'length': length,
        'art_style': art_style
    }


def get_demo_story():
    """Return a demo story idea."""
    
    return {
        'plot': 'A plump, witty kid named Leo uses kindness and humor to make friends at a new school, starting with a lonely kid on the Friendship Bench.',
        'target_age': '8-12',
        'themes': ['friendship', 'kindness', 'courage', 'humor'],
        'length': 'short',
        'art_style': 'children_book'
    }


if __name__ == '__main__':
    main()
