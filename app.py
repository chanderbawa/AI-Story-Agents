#!/usr/bin/env python3
"""
Simple launcher for AI Story Agents Web Interface
Perfect for Google Colab and local deployment
"""

from web_interface import StoryWebInterface

if __name__ == '__main__':
    # Create and launch the web interface
    print("🚀 Starting AI Story Agents Web Interface...")
    print("=" * 60)
    
    web_interface = StoryWebInterface(config_path='config/agents_config.yaml')
    
    # Launch with share=True for Colab (creates public link)
    # Set to False for local-only access
    web_interface.launch(share=True, server_port=7860)
