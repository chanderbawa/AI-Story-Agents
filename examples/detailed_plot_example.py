#!/usr/bin/env python3
"""
Example: Creating a story with a detailed, structured plot
Demonstrates how to write plots for maximum AI adherence
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.coordinator import StoryOrchestrator


def create_story_with_detailed_plot():
    """
    Example of a well-structured plot that the AI will follow closely.
    
    This plot is ~1800 characters - the sweet spot for adherence.
    """
    
    # Detailed, structured plot
    detailed_plot = """
CHARACTERS:
- Leo Martinez: A plump, witty 9-year-old with curly brown hair and expressive eyes. 
  New to Oakwood Elementary. Uses humor to cope with nervousness. Loves comic books 
  and drawing superheroes.
  
- Maya Chen: A quiet 8-year-old with long black hair and glasses. Sits alone on the 
  Friendship Bench. Excellent artist but shy about sharing her work. Draws manga-style 
  characters.
  
- Jake: The "popular" kid who sometimes teases others but isn't truly mean.

SETTING:
Oakwood Elementary School, first week of 4th grade, September. The school has a 
special "Friendship Bench" painted bright yellow where kids sit when they want 
someone to play with.

PLOT:
Leo is terrified on his first day at a new school. During recess, he notices Maya 
sitting alone on the Friendship Bench, looking sad. Despite his own fears, Leo 
decides to approach her, using a joke: "Is this the VIP section? Because this 
bench looks way too fancy for regular kids."

Maya is surprised but laughs. They discover they both love drawing and comic books. 
Leo shows Maya his superhero sketches, and Maya shares her manga-style drawings. 
They spend the rest of recess planning a comic book together.

CONFLICT:
The next day at lunch, Jake and his friends make fun of Leo's weight. Leo tries 
to laugh it off with a joke, but he's clearly hurt. Maya, despite being shy, 
stands up for Leo, telling Jake that real friends don't make fun of each other. 
Her courage surprises everyone, including herself.

RESOLUTION:
Inspired by Maya's bravery, Leo suggests they start a comic book club that meets 
at the Friendship Bench. By Friday, five other kids have joined - all kids who 
felt like outsiders. The Friendship Bench becomes their headquarters. Leo realizes 
that being kind and brave matters more than being popular.

KEY SCENES TO INCLUDE:
1. Leo's nervous first morning, walking into the school
2. Leo approaching Maya at the Friendship Bench with his joke
3. Leo and Maya discovering their shared love of comics in the library
4. The lunch incident with Jake's teasing
5. Maya's brave moment standing up for Leo
6. The first comic book club meeting with all five new friends

THEMES:
- Kindness can overcome fear
- True friendship means standing up for each other
- Being different is okay and can be a strength
- Humor can help in difficult situations
- Small acts of courage can inspire others

TONE:
Warm, humorous, uplifting. Show Leo's wit through dialogue. Include moments of 
vulnerability but always end scenes on a hopeful note. Use short, punchy sentences 
for action and longer ones for emotional moments.

DIALOGUE EXAMPLES:
- Leo's opening: "Is this the VIP section? Because this bench looks way too fancy."
- Maya's brave moment: "That's not funny, Jake. Leo is my friend."
- Leo's realization: "You know what? The best friends are the ones who see you."
"""

    # Story configuration
    story_idea = {
        'plot': detailed_plot,
        'target_age': '8-12',
        'themes': ['friendship', 'kindness', 'courage', 'humor'],
        'length': 'short',  # 3 chapters
        'art_style': 'children_book'
    }
    
    print("=" * 70)
    print("CREATING STORY WITH DETAILED PLOT")
    print("=" * 70)
    print(f"\nPlot length: {len(detailed_plot)} characters")
    print(f"Target age: {story_idea['target_age']}")
    print(f"Themes: {', '.join(story_idea['themes'])}")
    print(f"Length: {story_idea['length']}")
    print("\n" + "=" * 70)
    
    # Initialize orchestrator
    print("\n🎬 Initializing AI Story Agents...")
    orchestrator = StoryOrchestrator()
    
    # Generate story
    print("\n📖 Generating story...")
    print("⏱️  This will take approximately 5-15 minutes (GPU) or 30-45 minutes (CPU)")
    print("\n" + "=" * 70 + "\n")
    
    result = orchestrator.create_story(story_idea)
    
    # Check result
    print("\n" + "=" * 70)
    if result['status'] == 'complete':
        print("✅ STORY GENERATION COMPLETE!")
        print("=" * 70)
        print(f"\n📊 Story Statistics:")
        print(f"   Title: {result['metadata'].get('title', 'Untitled Story')}")
        print(f"   Chapters: {result['metadata']['chapters']}")
        print(f"   Illustrations: {result['metadata']['images']}")
        print(f"   Pages: {result['metadata']['page_count']}")
        print(f"\n📁 Output Files:")
        for format_type, filepath in result['publications'].items():
            print(f"   {format_type.upper()}: {filepath}")
        print("\n🎉 Your illustrated story book is complete!")
        
        # Verification checklist
        print("\n📋 Verification Checklist:")
        print("   Check that the story includes:")
        print("   [ ] Characters: Leo and Maya with described traits")
        print("   [ ] Setting: Oakwood Elementary and Friendship Bench")
        print("   [ ] Key scenes: First meeting, comic discovery, lunch incident")
        print("   [ ] Conflict: Jake's teasing")
        print("   [ ] Resolution: Comic book club formation")
        print("   [ ] Themes: Friendship, courage, kindness evident")
        
    else:
        print("❌ STORY GENERATION FAILED")
        print("=" * 70)
        print(f"Error: {result.get('message', 'Unknown error')}")
    
    return result


def create_story_with_minimal_plot():
    """
    Example of a minimal plot (for comparison).
    
    This will work but the AI will improvise more details.
    """
    
    minimal_plot = "A kid makes friends at a new school."
    
    story_idea = {
        'plot': minimal_plot,
        'target_age': '8-12',
        'themes': ['friendship'],
        'length': 'short',
        'art_style': 'children_book'
    }
    
    print("=" * 70)
    print("CREATING STORY WITH MINIMAL PLOT (FOR COMPARISON)")
    print("=" * 70)
    print(f"\nPlot: {minimal_plot}")
    print(f"Plot length: {len(minimal_plot)} characters")
    print("\nNote: The AI will improvise most details.")
    print("=" * 70)
    
    orchestrator = StoryOrchestrator()
    result = orchestrator.create_story(story_idea)
    
    return result


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate story with detailed plot')
    parser.add_argument(
        '--minimal',
        action='store_true',
        help='Use minimal plot instead (for comparison)'
    )
    
    args = parser.parse_args()
    
    if args.minimal:
        result = create_story_with_minimal_plot()
    else:
        result = create_story_with_detailed_plot()
