"""
Advanced Workflow Example
Demonstrates custom agent interactions and workflows.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.coordinator import StoryOrchestrator
from agents import Message


def create_story_with_custom_workflow():
    """Create a story with custom agent interactions."""
    
    print("🎬 Advanced Workflow Example")
    print("=" * 60)
    
    # Custom configuration
    config = {
        'author': {
            'model_name': 'mistralai/Mistral-7B-Instruct-v0.2',
            'device': 'auto',
            'load_in_8bit': True,
            'temperature': 0.8,  # More creative
            'writing_style': 'humorous',
            'load_model': False  # Testing mode
        },
        'illustrator': {
            'model_name': 'runwayml/stable-diffusion-v1-5',
            'art_style': 'cartoon',
            'num_inference_steps': 30,  # Faster generation
            'load_model': False
        },
        'publisher': {
            'formats': ['pdf', 'html'],
        },
        'output_dir': 'output/custom_stories'
    }
    
    orchestrator = StoryOrchestrator(config)
    
    # Complex story idea
    story_idea = {
        'plot': '''A group of misfit robots in a junkyard discover they have unique 
                   talents and form a band to save their home from demolition''',
        'target_age': '10-14',
        'themes': ['teamwork', 'creativity', 'perseverance', 'found family'],
        'length': 'medium',
        'art_style': 'cartoon'
    }
    
    print(f"\n📖 Creating story: {story_idea['plot'][:60]}...")
    
    # Monitor agent communication
    print("\n🔄 Agent Communication Log:")
    print("-" * 60)
    
    # Create story with monitoring
    result = orchestrator.create_story(story_idea)
    
    # Show agent statuses
    print("\n📊 Agent Status:")
    statuses = orchestrator.get_agent_status()
    for agent_name, status in statuses.items():
        print(f"   {agent_name}: {status}")
    
    # Show agent memory/interactions
    print("\n💭 Agent Interactions:")
    for agent_name, agent in orchestrator.agents.items():
        messages = agent.get_context(limit=5)
        print(f"\n   {agent_name} ({len(messages)} recent messages):")
        for msg in messages[-3:]:  # Show last 3
            print(f"      {msg.sender} → {msg.recipient}: {msg.message_type}")
    
    if result['status'] == 'complete':
        print("\n✅ Story created successfully!")
        
        # Detailed results
        print(f"\n📚 Story Details:")
        print(f"   Title: {result['metadata'].get('title', 'Untitled')}")
        print(f"   Chapters: {result['metadata']['chapters']}")
        print(f"   Illustrations: {result['metadata']['images']}")
        print(f"   Estimated Pages: {result['metadata']['page_count']}")
        
        # Show chapter titles
        if 'story' in result:
            print(f"\n📖 Chapter Titles:")
            for chapter in result['story'].get('chapters', []):
                print(f"      {chapter.get('number')}. {chapter.get('title', 'Untitled')}")
        
        print(f"\n📁 Publications:")
        for format_type, filepath in result['publications'].items():
            print(f"   {format_type.upper()}: {filepath}")
    
    return result


def demonstrate_agent_collaboration():
    """Show how agents collaborate and communicate."""
    
    print("\n\n🤝 Agent Collaboration Demo")
    print("=" * 60)
    
    orchestrator = StoryOrchestrator()
    
    # Simulate agent interaction
    print("\n1️⃣ Author creates a scene description...")
    scene = {
        'id': 'demo_scene_1',
        'description': 'A robot stands in a junkyard',
        'characters': ['Rusty the Robot'],
        'mood': 'lonely'
    }
    
    print("\n2️⃣ Illustrator requests more details...")
    # Illustrator finds description too vague
    feedback = orchestrator.illustrator.provide_feedback_to_author(scene)
    print(f"   Feedback: {feedback}")
    
    if feedback['clarity'] == 'needs_improvement':
        print(f"   Missing details: {', '.join(feedback['missing_details'])}")
        print("\n3️⃣ Illustrator requests clarification from Author...")
        
        # In real workflow, this would trigger author to enhance description
        enhanced_scene = {
            **scene,
            'description': '''Rusty the Robot stands alone in the center of a vast junkyard, 
                             surrounded by piles of scrap metal and old car parts. 
                             The setting sun casts long shadows. Rusty's posture is slumped, 
                             and his optical sensors glow dimly with a blue light.'''
        }
        
        print("\n4️⃣ Author provides enhanced description...")
        print(f"   Enhanced: {enhanced_scene['description'][:100]}...")
        
        print("\n5️⃣ Illustrator proceeds with generation...")
        print("   ✅ Scene clarity improved - generating illustration")
    
    print("\n✅ Collaboration complete!")


if __name__ == '__main__':
    # Run advanced workflow
    result = create_story_with_custom_workflow()
    
    # Demonstrate collaboration
    demonstrate_agent_collaboration()
