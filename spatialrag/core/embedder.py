# spatialrag/core/embedder.py
from transformers import AutoModel
import torch
from typing import List, Union
import numpy as np

class JinaV4Embedder:
    """State-of-the-art multi-modal embeddings"""
    
    def __init__(self):
        self.model = AutoModel.from_pretrained(
            "jinaai/jina-embeddings-v4",
            trust_remote_code=True,
            device_map="auto"
        )
        
    def embed_multimodal_context(self, context_block: Dict) -> np.ndarray:
        """Embed your multi-context blocks with spatial awareness"""
        
        # Combine text elements with spatial metadata
        text_parts = []
        
        if context_block.get('primary_heading'):
            text_parts.append(f"# {context_block['primary_heading']['text']}")
        
        if context_block.get('surrounding_paragraphs'):
            text_parts.extend(context_block['surrounding_paragraphs'])
            
        if context_block.get('caption'):
            text_parts.append(f"Caption: {context_block['caption']}")
        
        # Create unified text representation
        unified_text = "\n\n".join(text_parts)
        
        # Add spatial metadata as structured text
        spatial_info = f"[SPATIAL] Confidence: {context_block.get('spatial_confidence', 0):.2f}"
        final_text = f"{unified_text}\n{spatial_info}"
        
        # Generate embedding with Jina v4
        return self.model.encode(final_text, convert_to_numpy=True)
