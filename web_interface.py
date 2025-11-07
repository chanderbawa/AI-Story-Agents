#!/usr/bin/env python3
"""
Web Interface for AI Story Agents
Provides a user-friendly Gradio interface for story creation
"""

import gradio as gr
import os
import sys
from pathlib import Path
from typing import Tuple, Optional
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from orchestrator.coordinator import StoryOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebInterface")


class StoryWebInterface:
    """Web interface for AI Story Agents using Gradio."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the web interface."""
        self.config_path = config_path
        self.orchestrator = None
        self.output_dir = Path("output/publications")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def initialize_orchestrator(self):
        """Lazy initialization of orchestrator to save memory."""
        if self.orchestrator is None:
            logger.info("🎬 Initializing AI Story Agents...")
            config = None
            if self.config_path and Path(self.config_path).exists():
                import yaml
                with open(self.config_path, 'r') as f:
                    config = yaml.safe_load(f)
            self.orchestrator = StoryOrchestrator(config)
            logger.info("✅ Agents ready!")
        return self.orchestrator
    
    def create_story_from_web(
        self,
        plot: str,
        themes: str,
        target_age: str,
        length: str,
        art_style: str,
        progress=gr.Progress()
    ) -> Tuple[str, str, str]:
        """
        Create a story from web interface inputs.
        
        Returns:
            Tuple of (status_message, pdf_path, preview_html)
        """
        try:
            # Validate inputs
            if not plot or len(plot.strip()) < 10:
                return "❌ Please provide a story plot (at least 10 characters)", None, ""
            
            # Parse themes
            theme_list = [t.strip() for t in themes.split(',') if t.strip()]
            if not theme_list:
                theme_list = ['friendship', 'courage']
            
            # Initialize orchestrator
            progress(0.1, desc="Initializing AI agents...")
            orchestrator = self.initialize_orchestrator()
            
            # Prepare story idea
            story_idea = {
                'plot': plot.strip(),
                'target_age': target_age,
                'themes': theme_list,
                'length': length.lower(),
                'art_style': art_style.lower().replace(' ', '_')
            }
            
            logger.info(f"📖 Creating story: {plot[:50]}...")
            
            # Create story
            progress(0.2, desc="Writing story...")
            result = orchestrator.create_story(story_idea)
            
            if result['status'] == 'complete':
                # Get PDF path
                pdf_path = result['publications'].get('pdf', '')
                
                # Create preview HTML
                metadata = result['metadata']
                preview_html = f"""
                <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            border-radius: 10px; color: white; margin: 10px 0;">
                    <h2 style="margin-top: 0;">✅ Story Created Successfully!</h2>
                    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin: 10px 0;">
                        <p style="margin: 5px 0;"><strong>📊 Statistics:</strong></p>
                        <ul style="margin: 10px 0; padding-left: 20px;">
                            <li>Chapters: {metadata.get('chapters', 0)}</li>
                            <li>Illustrations: {metadata.get('images', 0)}</li>
                            <li>Pages: {metadata.get('page_count', 0)}</li>
                        </ul>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin: 10px 0;">
                        <p style="margin: 5px 0;"><strong>📁 Output Files:</strong></p>
                        <ul style="margin: 10px 0; padding-left: 20px;">
                """
                
                for format_type, filepath in result['publications'].items():
                    preview_html += f"<li>{format_type.upper()}: {filepath}</li>"
                
                preview_html += """
                        </ul>
                    </div>
                    <p style="margin-bottom: 0;">🎉 Download your PDF below!</p>
                </div>
                """
                
                success_msg = f"""
✅ **Story Creation Complete!**

📖 **Title:** {metadata.get('title', 'Untitled Story')}
📊 **Stats:** {metadata.get('chapters', 0)} chapters, {metadata.get('images', 0)} illustrations, {metadata.get('page_count', 0)} pages

📥 **Download your PDF below!**
                """
                
                return success_msg, pdf_path, preview_html
            else:
                error_msg = result.get('message', 'Unknown error occurred')
                return f"❌ Story creation failed: {error_msg}", None, ""
                
        except Exception as e:
            logger.error(f"Error creating story: {str(e)}", exc_info=True)
            return f"❌ Error: {str(e)}", None, ""
    
    def create_demo_story(self, progress=gr.Progress()) -> Tuple[str, str, str]:
        """Create a demo story with predefined settings."""
        demo_plot = "A plump, witty kid named Leo uses kindness and humor to make friends at a new school, starting with a lonely kid on the Friendship Bench."
        return self.create_story_from_web(
            plot=demo_plot,
            themes="friendship, kindness, courage, humor",
            target_age="8-12",
            length="short",
            art_style="children_book",
            progress=progress
        )
    
    def build_interface(self) -> gr.Blocks:
        """Build and return the Gradio interface."""
        
        with gr.Blocks(
            theme=gr.themes.Soft(),
            title="AI Story Agents - Create Illustrated Stories",
            css="""
            .gradio-container {max-width: 1200px !important;}
            .header {text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     color: white; border-radius: 10px; margin-bottom: 20px;}
            .footer {text-align: center; padding: 10px; color: #666; margin-top: 20px;}
            """
        ) as interface:
            
            # Header
            gr.HTML("""
                <div class="header">
                    <h1>🤖 AI Story Agents</h1>
                    <p style="font-size: 18px; margin: 10px 0;">Create Illustrated Children's Books with AI</p>
                    <p style="font-size: 14px; opacity: 0.9;">Multi-agent system featuring Author, Illustrator, and Publisher agents</p>
                </div>
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("## 📝 Story Details")
                    
                    plot_input = gr.Textbox(
                        label="Story Plot/Idea",
                        placeholder="Enter your story idea here... (e.g., 'A shy kid discovers they can talk to animals and helps save the school garden')",
                        lines=5,
                        info="Describe the main plot, characters, or theme of your story"
                    )
                    
                    with gr.Row():
                        themes_input = gr.Textbox(
                            label="Themes",
                            placeholder="friendship, courage, adventure",
                            value="friendship, courage",
                            info="Comma-separated themes"
                        )
                        
                        age_input = gr.Dropdown(
                            label="Target Age",
                            choices=["5-7", "8-12", "10-14"],
                            value="8-12",
                            info="Age range for readers"
                        )
                    
                    with gr.Row():
                        length_input = gr.Radio(
                            label="Story Length",
                            choices=["Short", "Medium", "Long"],
                            value="Short",
                            info="Short: 3 chapters, Medium: 5 chapters, Long: 8 chapters"
                        )
                        
                        style_input = gr.Dropdown(
                            label="Art Style",
                            choices=["Children Book", "Cartoon", "Watercolor", "Line Art"],
                            value="Children Book",
                            info="Visual style for illustrations"
                        )
                    
                    with gr.Row():
                        create_btn = gr.Button("🚀 Create Story", variant="primary", size="lg")
                        demo_btn = gr.Button("🎬 Try Demo", variant="secondary", size="lg")
                    
                    gr.Markdown("""
                    ### 💡 Tips:
                    - Be specific about characters and settings
                    - Include conflict or challenge in your plot
                    - Consider your target audience's interests
                    - Story generation may take 5-15 minutes depending on length
                    """)
                
                with gr.Column(scale=1):
                    gr.Markdown("## 📚 Story Output")
                    
                    status_output = gr.Markdown(
                        value="*Enter a story idea and click 'Create Story' to begin...*"
                    )
                    
                    preview_output = gr.HTML()
                    
                    pdf_output = gr.File(
                        label="📥 Download PDF",
                        file_types=[".pdf"],
                        type="filepath"
                    )
                    
                    gr.Markdown("""
                    ### 📖 What Happens Next:
                    1. **Author Agent** writes your story with engaging narrative
                    2. **Illustrator Agent** creates beautiful illustrations
                    3. **Publisher Agent** assembles everything into a PDF
                    4. Download your complete illustrated book!
                    
                    ### ⚙️ Technical Details:
                    - Uses advanced AI models (LLMs + Stable Diffusion)
                    - Generates consistent characters across illustrations
                    - Professional PDF layout with typography
                    - GPU acceleration recommended (works on CPU too)
                    """)
            
            # Footer
            gr.HTML("""
                <div class="footer">
                    <p>Built with ❤️ using Gradio | Multi-Agent AI System</p>
                    <p style="font-size: 12px;">Author Agent • Illustrator Agent • Publisher Agent</p>
                </div>
            """)
            
            # Event handlers
            create_btn.click(
                fn=self.create_story_from_web,
                inputs=[plot_input, themes_input, age_input, length_input, style_input],
                outputs=[status_output, pdf_output, preview_output],
                api_name="create_story"
            )
            
            demo_btn.click(
                fn=self.create_demo_story,
                inputs=[],
                outputs=[status_output, pdf_output, preview_output],
                api_name="demo_story"
            )
        
        return interface
    
    def launch(self, share: bool = False, server_port: int = 7860):
        """Launch the web interface."""
        interface = self.build_interface()
        
        logger.info("🌐 Launching web interface...")
        logger.info(f"📍 Access at: http://localhost:{server_port}")
        
        if share:
            logger.info("🔗 Creating public share link...")
        
        interface.launch(
            share=share,
            server_port=server_port,
            server_name="0.0.0.0",
            show_error=True,
            quiet=False
        )


def main():
    """Main entry point for web interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Story Agents Web Interface")
    parser.add_argument(
        '--config',
        type=str,
        default='config/agents_config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--share',
        action='store_true',
        help='Create a public share link'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=7860,
        help='Server port (default: 7860)'
    )
    
    args = parser.parse_args()
    
    # Create and launch interface
    web_interface = StoryWebInterface(config_path=args.config)
    web_interface.launch(share=args.share, server_port=args.port)


if __name__ == '__main__':
    main()
