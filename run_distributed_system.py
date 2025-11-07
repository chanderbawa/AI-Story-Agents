#!/usr/bin/env python3
"""
Launch all agent services and orchestrator
"""

import subprocess
import time
import sys
import signal
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

logger = logging.getLogger(__name__)

processes = []

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    logger.info("\n🛑 Shutting down all services...")
    for proc in processes:
        proc.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    print("="*70)
    print("🚀 DISTRIBUTED AI STORY AGENTS SYSTEM")
    print("="*70)
    print("\nStarting all services...")
    print()
    
    # Start Author Service
    logger.info("📝 Starting Author Service (port 8001)...")
    author_proc = subprocess.Popen(
        [sys.executable, 'run_author_service.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    processes.append(author_proc)
    time.sleep(3)
    
    # Start Illustrator Service
    logger.info("🎨 Starting Illustrator Service (port 8002)...")
    illustrator_proc = subprocess.Popen(
        [sys.executable, 'run_illustrator_service.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    processes.append(illustrator_proc)
    time.sleep(3)
    
    # Start Publisher Service
    logger.info("📚 Starting Publisher Service (port 8003)...")
    publisher_proc = subprocess.Popen(
        [sys.executable, 'run_publisher_service.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    processes.append(publisher_proc)
    time.sleep(3)
    
    print()
    print("="*70)
    print("✅ ALL SERVICES RUNNING")
    print("="*70)
    print("\n📍 Service Endpoints:")
    print("   Author:      http://localhost:8001")
    print("   Illustrator: http://localhost:8002")
    print("   Publisher:   http://localhost:8003")
    print("\n💡 Usage:")
    print("   python distributed_client.py --plot 'Your story idea'")
    print("\n🔍 Health Checks:")
    print("   curl http://localhost:8001/health")
    print("   curl http://localhost:8002/health")
    print("   curl http://localhost:8003/health")
    print("\nPress Ctrl+C to stop all services")
    print("="*70)
    print()
    
    # Keep running
    try:
        while True:
            time.sleep(1)
            # Check if any process died
            for i, proc in enumerate(processes):
                if proc.poll() is not None:
                    logger.error(f"❌ Service {i} died! Exit code: {proc.returncode}")
                    # Restart it
                    logger.info(f"🔄 Restarting service {i}...")
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
