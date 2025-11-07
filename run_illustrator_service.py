#!/usr/bin/env python3
"""
Launch Illustrator Agent as a standalone service
"""

import argparse
import logging
from distributed.agent_service import run_illustrator_service

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Illustrator Agent Service')
    parser.add_argument('--port', type=int, default=8002, help='Service port')
    parser.add_argument('--config', type=str, default='config/agents_config.yaml',
                       help='Config file path')
    
    args = parser.parse_args()
    
    print("="*70)
    print("🎨 ILLUSTRATOR AGENT SERVICE")
    print("="*70)
    print(f"Port: {args.port}")
    print(f"Config: {args.config}")
    print("="*70)
    print("\n🚀 Starting service...")
    print(f"   API: http://localhost:{args.port}")
    print(f"   Health: http://localhost:{args.port}/health")
    print("\nPress Ctrl+C to stop\n")
    
    run_illustrator_service(port=args.port, config_path=args.config)
