#!/usr/bin/env python3
"""
Diagnostic script to test story generation and identify issues
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_model_loading():
    """Test if models load correctly"""
    print("="*70)
    print("TEST 1: Model Loading")
    print("="*70)
    
    try:
        from agents.author_agent import AuthorAgent
        import yaml
        
        # Load CPU config
        with open('config/agents_config_cpu.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        print("\n📦 Loading Author Agent...")
        author = AuthorAgent(config['author'])
        
        if author.generator:
            print("✅ Author model loaded successfully")
            print(f"   Model: {config['author']['model_name']}")
        else:
            print("❌ Author model failed to load")
            return False
            
    except Exception as e:
        print(f"❌ Error loading models: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_text_generation():
    """Test basic text generation"""
    print("\n" + "="*70)
    print("TEST 2: Text Generation")
    print("="*70)
    
    try:
        from agents.author_agent import AuthorAgent
        import yaml
        
        with open('config/agents_config_cpu.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        author = AuthorAgent(config['author'])
        
        # Simple test prompt
        test_prompt = "Write a short paragraph about a brave mouse named Max."
        
        print(f"\n📝 Test Prompt: {test_prompt}")
        print("\n⏱️  Generating (this may take 30-60 seconds on CPU)...")
        
        result = author._generate_text(test_prompt, max_length=100)
        
        print(f"\n📄 Generated Text ({len(result)} characters):")
        print("-" * 70)
        print(result)
        print("-" * 70)
        
        if len(result) < 20:
            print("\n⚠️  WARNING: Generated text is very short!")
            print("   This indicates a problem with text generation.")
            return False
        else:
            print("\n✅ Text generation working")
            return True
            
    except Exception as e:
        print(f"\n❌ Error during text generation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_chapter_generation():
    """Test full chapter generation"""
    print("\n" + "="*70)
    print("TEST 3: Chapter Generation")
    print("="*70)
    
    try:
        from agents.author_agent import AuthorAgent
        import yaml
        
        with open('config/agents_config_cpu.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        author = AuthorAgent(config['author'])
        
        # Test chapter outline
        outline = {
            'title': 'The Beginning',
            'events': 'Max the mouse discovers a map to magical cheese'
        }
        
        characters = [
            {'name': 'Max', 'personality': 'brave and curious'}
        ]
        
        print("\n📖 Generating test chapter...")
        print("⏱️  This may take 2-3 minutes on CPU...")
        
        chapter = author._write_chapter(1, outline, characters)
        
        print(f"\n📄 Chapter Text ({len(chapter['text'])} characters):")
        print("-" * 70)
        print(chapter['text'][:500] + "..." if len(chapter['text']) > 500 else chapter['text'])
        print("-" * 70)
        
        if len(chapter['text']) < 100:
            print("\n⚠️  WARNING: Chapter text is too short!")
            return False
        else:
            print(f"\n✅ Chapter generation working ({len(chapter['text'])} characters)")
            return True
            
    except Exception as e:
        print(f"\n❌ Error during chapter generation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n🔍 AI STORY AGENTS - DIAGNOSTIC TOOL")
    print("="*70)
    print("This will test the story generation pipeline and identify issues.")
    print("="*70)
    
    results = {
        'model_loading': False,
        'text_generation': False,
        'chapter_generation': False
    }
    
    # Run tests
    results['model_loading'] = test_model_loading()
    
    if results['model_loading']:
        results['text_generation'] = test_text_generation()
        
        if results['text_generation']:
            results['chapter_generation'] = test_chapter_generation()
    
    # Summary
    print("\n" + "="*70)
    print("DIAGNOSTIC SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name.replace('_', ' ').title()}")
    
    print("="*70)
    
    if all(results.values()):
        print("\n✅ All tests passed! Story generation should work.")
        print("\n💡 If you're still having issues, the problem may be:")
        print("   1. Plot is too long or complex")
        print("   2. Not enough RAM/memory")
        print("   3. Model needs more time to generate")
    else:
        print("\n❌ Some tests failed. Issues detected:")
        if not results['model_loading']:
            print("   • Model loading failed - check dependencies")
        if not results['text_generation']:
            print("   • Text generation failed - model may not be working")
        if not results['chapter_generation']:
            print("   • Chapter generation failed - check prompts/config")
    
    print()

if __name__ == '__main__':
    main()
