#!/usr/bin/env python3
"""
CPU-Optimized launcher for AI Story Agents Web Interface
Use this for running on machines without GPU
"""

from web_interface import StoryWebInterface
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

if __name__ == '__main__':
    print("=" * 70)
    print("🖥️  AI STORY AGENTS - CPU MODE")
    print("=" * 70)
    print()
    print("⚙️  Configuration:")
    print("   • Using CPU-optimized models")
    print("   • TinyLlama for text generation (faster)")
    print("   • Stable Diffusion 1.5 with reduced steps")
    print("   • Smaller image dimensions (512x512)")
    print()
    print("⏱️  Expected Generation Time:")
    print("   • Short story: 30-45 minutes")
    print("   • Medium story: 45-60 minutes")
    print("   • Long story: 60-90 minutes")
    print()
    print("💡 Tips:")
    print("   • Start with SHORT stories to test")
    print("   • Close other applications to free up RAM")
    print("   • Be patient - CPU generation is slower but works!")
    print()
    print("=" * 70)
    print()
    
    # Create and launch interface with CPU config
    web_interface = StoryWebInterface(config_path='config/agents_config_cpu.yaml')
    
    print("🚀 Starting web interface on http://localhost:7860")
    print("   Press Ctrl+C to stop")
    print()
    
    # Launch without share link (local only)
    web_interface.launch(share=False, server_port=7860)
