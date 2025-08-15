# spatialrag/core/document_parser.py
from typing import Dict, List, Tuple
import pymupdf4llm
from docling import DocumentConverter
import fitz  # PyMuPDF for coordinates

class AdvancedDocumentParser:
    def __init__(self):
        self.converter = DocumentConverter()
    
    def parse_document(self, file_path: str) -> Dict:
        """Parse document with both structure and spatial info"""
        
        # Method 1: PyMuPDF4LLM for LLM-ready structure
        structured_text = pymupdf4llm.to_markdown(file_path)
        
        # Method 2: Extract spatial coordinates for images
        spatial_data = self._extract_spatial_data(file_path)
        
        # Method 3: Docling for enterprise-grade layout (fallback)
        layout_data = self.converter.convert(file_path)
        
        return {
            "structured_text": structured_text,
            "spatial_data": spatial_data,
            "layout_data": layout_data
        }
    
    def _extract_spatial_data(self, file_path: str) -> List[Dict]:
        """Extract image coordinates and nearby headings"""
        doc = fitz.open(file_path)
        spatial_elements = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get all text blocks with coordinates
            text_blocks = page.get_text("dict")["blocks"]
            headings = []
            
            for block in text_blocks:
                if block["type"] == 0:  # Text block
                    for line in block["lines"]:
                        text = "".join(span["text"] for span in line["spans"])
                        # Detect headings by font size/weight
                        if self._is_heading(line["spans"]):
                            headings.append({
                                "text": text.strip(),
                                "bbox": line["bbox"],
                                "level": self._get_heading_level(line["spans"])
                            })
            
            # Get images with coordinates
            for img_index, img in enumerate(page.get_images()):
                img_rect = page.get_image_bbox(img)
                nearest_heading = self._find_nearest_heading(img_rect, headings)
                
                spatial_elements.append({
                    "type": "image",
                    "bbox": img_rect,
                    "page": page_num,
                    "nearest_heading": nearest_heading,
                    "image_index": img_index
                })
        
        return spatial_elements
