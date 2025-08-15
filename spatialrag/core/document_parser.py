# spatialrag/core/document_parser.py
from typing import Dict, List
import pymupdf4llm
import fitz  # PyMuPDF for coordinates

class AdvancedDocumentParser:
    def __init__(self):
        pass  # Removed docling usage for now
    
    def parse_document(self, file_path: str) -> Dict:
        """Parse document with structure and spatial info using PyMuPDF4LLM and PyMuPDF"""
        
        # Method 1: PyMuPDF4LLM for LLM-ready structured markdown extraction
        structured_text = pymupdf4llm.to_markdown(file_path)
        
        # Method 2: Extract spatial coordinates for images and headings
        spatial_data = self._extract_spatial_data(file_path)
        
        return {
            "structured_text": structured_text,
            "spatial_data": spatial_data,
        }
    
    def _extract_spatial_data(self, file_path: str) -> List[Dict]:
        """Extract image coordinates and nearest headings"""
        doc = fitz.open(file_path)
        spatial_elements = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get all text blocks with coordinates for heading detection
            text_blocks = page.get_text("dict")["blocks"]
            headings = []
            
            for block in text_blocks:
                if block["type"] == 0:  # Text block
                    for line in block["lines"]:
                        text = "".join(span["text"] for span in line["spans"]).strip()
                        if self._is_heading(line["spans"], text):
                            headings.append({
                                "text": text,
                                "bbox": line["bbox"],
                                "level": self._get_heading_level(line["spans"])
                            })
            
            # Get images with their bounding boxes and associate nearest heading
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                img_rect = page.get_image_bbox(img)
                nearest_heading = self._find_nearest_heading(img_rect, headings)
                
                spatial_elements.append({
                    "type": "image",
                    "bbox": img_rect,
                    "page": page_num,
                    "nearest_heading": nearest_heading,
                    "image_index": img_index,
                    "xref": xref
                })
        
        return spatial_elements
    
    def _is_heading(self, spans, text: str) -> bool:
        """Simple heuristic: font size larger than threshold and non-empty"""
        if not text:
            return False
        # Example threshold: font size greater than 11pt
        avg_fontsize = sum(span["size"] for span in spans) / len(spans) if spans else 0
        return avg_fontsize > 11 and len(text) < 100  # Avoid long paragraphs
    
    def _get_heading_level(self, spans) -> int:
        """Heuristic for heading level based on size"""
        avg_fontsize = sum(span["size"] for span in spans) / len(spans) if spans else 10
        if avg_fontsize >= 18:
            return 1
        elif avg_fontsize >= 14:
            return 2
        else:
            return 3
    
    def _find_nearest_heading(self, img_rect, headings: List[Dict]) -> Dict:
        """Find nearest heading by vertical distance"""
        min_distance = float('inf')
        nearest = None
        for heading in headings:
            heading_y = heading["bbox"][1]  # y0 top coordinate
            distance = abs(heading_y - img_rect.y0)
            if distance < min_distance:
                min_distance = distance
                nearest = heading
        return nearest

