#!/usr/bin/env python3
"""
Quick test script for the web interface
Tests that the interface can be built without errors
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_web_interface():
    """Test that the web interface can be initialized."""
    print("🧪 Testing Web Interface...")
    print("=" * 60)
    
    try:
        # Import the web interface
        from web_interface import StoryWebInterface
        print("✅ Web interface module imported successfully")
        
        # Create interface instance (without loading models)
        web_interface = StoryWebInterface()
        print("✅ Web interface instance created")
        
        # Build the Gradio interface
        interface = web_interface.build_interface()
        print("✅ Gradio interface built successfully")
        
        print("\n" + "=" * 60)
        print("🎉 All tests passed!")
        print("=" * 60)
        print("\n📝 To launch the web interface, run:")
        print("   python app.py")
        print("\n🌐 For Google Colab, see COLAB_SETUP.md")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_web_interface()
    sys.exit(0 if success else 1)
