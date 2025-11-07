"""
Publisher Agent - Production Manager
Assembles stories and illustrations into publication-ready formats.
"""

from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, Message
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas
import os
from datetime import datetime


class PublisherAgent(BaseAgent):
    """
    AI agent specialized in publishing and production.
    
    Capabilities:
    - PDF assembly and layout
    - Typography and formatting
    - Multi-format export (PDF, EPUB, HTML)
    - Quality control
    - Production coordination
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            name="PublisherAgent",
            role="Production Manager & Publisher",
            config=config
        )
        
        self.layout_config = config.get('layout', {})
        self.output_formats = config.get('formats', ['pdf'])
        
        # Publication metadata
        self.current_publication = {
            'title': '',
            'author': 'AI Story Agents',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'chapters': [],
            'images': []
        }
    
    def process_message(self, message: Message) -> Optional[Message]:
        """Process messages from other agents."""
        
        if message.message_type == "request":
            if message.content.get('action') == 'publish':
                # Orchestrator requesting publication
                result = self.execute_task(message.content)
                return self.send_message(
                    message.sender,
                    result,
                    "response"
                )
            
            elif message.content.get('action') == 'preview':
                # Generate preview/proof
                preview = self._create_preview(message.content)
                return self.send_message(
                    message.sender,
                    {'preview': preview},
                    "response"
                )
        
        return None
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main task execution for publication.
        
        Args:
            task: Contains story, images, format specifications
            
        Returns:
            Publication results with file paths
        """
        self.update_status("working", "Assembling publication...")
        
        story = task.get('story', {})
        images = task.get('images', [])
        output_dir = task.get('output_dir', 'output/publications')
        title = task.get('title', story.get('plot', 'Untitled Story')[:50])
        
        # Store publication data
        self.current_publication['title'] = title
        self.current_publication['chapters'] = story.get('chapters', [])
        self.current_publication['images'] = images
        
        os.makedirs(output_dir, exist_ok=True)
        
        results = {}
        
        # Generate requested formats
        if 'pdf' in self.output_formats:
            self.logger.info("📚 Creating PDF...")
            pdf_path = self._create_pdf(output_dir, title)
            results['pdf'] = pdf_path
        
        if 'html' in self.output_formats:
            self.logger.info("🌐 Creating HTML...")
            html_path = self._create_html(output_dir, title)
            results['html'] = html_path
        
        if 'epub' in self.output_formats:
            self.logger.info("📖 Creating EPUB...")
            epub_path = self._create_epub(output_dir, title)
            results['epub'] = epub_path
        
        self.update_status("ready", f"Publication complete: {len(results)} formats")
        
        return {
            'status': 'complete',
            'files': results,
            'title': title,
            'page_count': self._estimate_page_count()
        }
    
    def _create_pdf(self, output_dir: str, title: str) -> str:
        """Create a professional PDF publication."""
        
        filename = f"{output_dir}/{self._sanitize_filename(title)}.pdf"
        
        # Page setup
        page_width = self.layout_config.get('page_width', 6) * inch
        page_height = self.layout_config.get('page_height', 9) * inch
        
        doc = SimpleDocTemplate(
            filename,
            pagesize=(page_width, page_height),
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch
        )
        
        # Styles
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#2C3E50',
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        chapter_style = ParagraphStyle(
            'ChapterTitle',
            parent=styles['Heading2'],
            fontSize=18,
            textColor='#34495E',
            spaceAfter=20,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=12,
            leading=18,
            alignment=TA_JUSTIFY,
            fontName='Times-Roman'
        )
        
        # Build document content
        story_elements = []
        
        # Title page
        story_elements.append(Spacer(1, 2 * inch))
        story_elements.append(Paragraph(self.current_publication['title'], title_style))
        story_elements.append(Spacer(1, 0.5 * inch))
        story_elements.append(Paragraph(
            f"By {self.current_publication['author']}", 
            styles['Normal']
        ))
        story_elements.append(PageBreak())
        
        # Chapters with images
        chapters = self.current_publication['chapters']
        images = self.current_publication['images']
        
        for chapter in chapters:
            # Chapter title
            story_elements.append(Paragraph(
                chapter.get('title', f"Chapter {chapter['number']}"),
                chapter_style
            ))
            story_elements.append(Spacer(1, 0.3 * inch))
            
            # Chapter text
            text = chapter.get('text', '')
            paragraphs = text.split('\n\n')
            
            for para in paragraphs:
                if para.strip():
                    story_elements.append(Paragraph(para, body_style))
                    story_elements.append(Spacer(1, 0.2 * inch))
            
            # Add images for this chapter
            chapter_images = [
                img for img in images 
                if img.get('chapter') == chapter['number']
            ]
            
            for img_data in chapter_images:
                story_elements.append(Spacer(1, 0.3 * inch))
                
                # Save PIL image temporarily
                img_path = f"{output_dir}/temp_img_{img_data['scene_id']}.png"
                img_data['image'].save(img_path)
                
                # Add to PDF
                img = Image(img_path, width=4 * inch, height=5.3 * inch)
                story_elements.append(img)
                story_elements.append(Spacer(1, 0.2 * inch))
                
                # Caption
                if 'description' in img_data:
                    caption = Paragraph(
                        f"<i>{img_data['description'][:100]}...</i>",
                        styles['Italic']
                    )
                    story_elements.append(caption)
            
            story_elements.append(PageBreak())
        
        # Build PDF
        doc.build(story_elements)
        
        self.logger.info(f"PDF created: {filename}")
        
        return filename
    
    def _create_html(self, output_dir: str, title: str) -> str:
        """Create an HTML version of the story."""
        
        filename = f"{output_dir}/{self._sanitize_filename(title)}.html"
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Georgia', serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            text-align: center;
            color: #2C3E50;
            font-size: 2.5em;
            margin-bottom: 0.5em;
        }}
        h2 {{
            color: #34495E;
            font-size: 1.8em;
            margin-top: 2em;
            border-bottom: 2px solid #3498DB;
            padding-bottom: 0.3em;
        }}
        p {{
            text-align: justify;
            margin-bottom: 1em;
        }}
        .image-container {{
            text-align: center;
            margin: 2em 0;
        }}
        .image-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .caption {{
            font-style: italic;
            color: #7F8C8D;
            margin-top: 0.5em;
        }}
        .author {{
            text-align: center;
            color: #7F8C8D;
            margin-bottom: 3em;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p class="author">By {self.current_publication['author']}</p>
"""
        
        # Add chapters
        for chapter in self.current_publication['chapters']:
            chapter_title = chapter.get('title', f"Chapter {chapter['number']}")
            html_content += f"\n    <h2>{chapter_title}</h2>\n"
            
            text = chapter.get('text', '')
            paragraphs = text.split('\n\n')
            
            for para in paragraphs:
                if para.strip():
                    html_content += f"    <p>{para}</p>\n"
            
            # Add images
            chapter_images = [
                img for img in self.current_publication['images']
                if img.get('chapter') == chapter['number']
            ]
            
            for img_data in chapter_images:
                img_filename = f"img_{img_data['scene_id']}.png"
                img_path = f"{output_dir}/{img_filename}"
                img_data['image'].save(img_path)
                
                html_content += f"""
    <div class="image-container">
        <img src="{img_filename}" alt="{img_data.get('description', 'Illustration')}">
        <p class="caption">{img_data.get('description', '')[:100]}</p>
    </div>
"""
        
        html_content += """
</body>
</html>
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.logger.info(f"HTML created: {filename}")
        
        return filename
    
    def _create_epub(self, output_dir: str, title: str) -> str:
        """Create an EPUB version (placeholder - requires ebooklib)."""
        
        filename = f"{output_dir}/{self._sanitize_filename(title)}.epub"
        
        # This would require ebooklib library
        # For now, create a placeholder
        self.logger.info(f"EPUB creation requires ebooklib - creating placeholder")
        
        with open(filename, 'w') as f:
            f.write("EPUB placeholder - install ebooklib for full functionality")
        
        return filename
    
    def _create_preview(self, data: Dict) -> str:
        """Create a quick preview/proof of the publication."""
        
        preview = f"""
=== PUBLICATION PREVIEW ===
Title: {self.current_publication['title']}
Author: {self.current_publication['author']}
Date: {self.current_publication['date']}

Chapters: {len(self.current_publication['chapters'])}
Images: {len(self.current_publication['images'])}
Estimated Pages: {self._estimate_page_count()}

=== CHAPTER SUMMARY ===
"""
        
        for chapter in self.current_publication['chapters']:
            word_count = len(chapter.get('text', '').split())
            preview += f"\n{chapter.get('title', 'Untitled')}: {word_count} words"
        
        return preview
    
    def _estimate_page_count(self) -> int:
        """Estimate total page count."""
        
        total_words = sum(
            len(ch.get('text', '').split()) 
            for ch in self.current_publication['chapters']
        )
        
        # Rough estimate: 250 words per page + images
        text_pages = total_words // 250
        image_pages = len(self.current_publication['images'])
        
        return text_pages + image_pages + 2  # +2 for title and extras
    
    def _sanitize_filename(self, filename: str) -> str:
        """Create safe filename from title."""
        
        import re
        # Remove invalid characters
        safe = re.sub(r'[^\w\s-]', '', filename)
        safe = re.sub(r'[-\s]+', '_', safe)
        return safe[:50]  # Limit length
    
    def get_capabilities(self) -> List[str]:
        """Return list of publisher capabilities."""
        return [
            'pdf_creation',
            'html_export',
            'epub_creation',
            'layout_design',
            'typography',
            'quality_control',
            'multi_format_export'
        ]
