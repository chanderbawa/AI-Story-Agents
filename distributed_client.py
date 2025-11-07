#!/usr/bin/env python3
"""
Client for distributed story generation system
"""

import argparse
import logging
from distributed.distributed_orchestrator import DistributedOrchestrator
from distributed.message_broker import get_broker

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(message)s'
)

def main():
    parser = argparse.ArgumentParser(description='Create story using distributed agents')
    parser.add_argument('--plot', type=str, required=True, help='Story plot/idea')
    parser.add_argument('--themes', type=str, nargs='+', default=['friendship', 'courage'],
                       help='Story themes')
    parser.add_argument('--age', type=str, default='8-12', help='Target age range')
    parser.add_argument('--length', type=str, default='short',
                       choices=['short', 'medium', 'long'], help='Story length')
    parser.add_argument('--style', type=str, default='children_book',
                       choices=['children_book', 'cartoon', 'watercolor', 'line_art'],
                       help='Art style')
    parser.add_argument('--timeout', type=int, default=1800,
                       help='Timeout in seconds (default: 1800 = 30 min)')
    
    args = parser.parse_args()
    
    print("="*70)
    print("📖 DISTRIBUTED STORY GENERATION CLIENT")
    print("="*70)
    print(f"\nPlot: {args.plot}")
    print(f"Themes: {', '.join(args.themes)}")
    print(f"Age: {args.age}")
    print(f"Length: {args.length}")
    print(f"Style: {args.style}")
    print("="*70)
    print()
    
    # Create story idea
    story_idea = {
        'plot': args.plot,
        'themes': args.themes,
        'target_age': args.age,
        'length': args.length,
        'art_style': args.style
    }
    
    # Initialize orchestrator
    broker = get_broker()
    orchestrator = DistributedOrchestrator(broker)
    
    print("🚀 Starting distributed story creation...")
    print("📊 Progress will be shown below:")
    print()
    
    # Create story
    result = orchestrator.create_story(story_idea, timeout=args.timeout)
    
    # Display result
    print()
    print("="*70)
    if result['status'] == 'complete':
        print("✅ STORY CREATION COMPLETE!")
        print("="*70)
        print(f"\n📊 Statistics:")
        print(f"   Chapters: {result.get('metadata', {}).get('chapters', 'N/A')}")
        print(f"   Images: {result.get('metadata', {}).get('images', 'N/A')}")
        print(f"   Pages: {result.get('metadata', {}).get('page_count', 'N/A')}")
        print(f"\n📁 Output Files:")
        for format_type, filepath in result.get('publications', {}).items():
            print(f"   {format_type.upper()}: {filepath}")
        print()
    else:
        print("❌ STORY CREATION FAILED")
        print("="*70)
        print(f"Status: {result['status']}")
        print(f"Message: {result.get('message', 'Unknown error')}")
        print()

if __name__ == '__main__':
    main()
