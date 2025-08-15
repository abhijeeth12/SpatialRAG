# spatialrag/core/spatial_mapper.py
from typing import Dict, List, Optional

class SpatialProximityMapper:
    """Spatial intelligence for documents"""

    def __init__(self, context_radius: int = 150):
        self.context_radius = context_radius

    def map_image_to_context(self, image_bbox, document_elements) -> Dict:
        """Map image to spatially relevant context blocks."""

        return {
            "primary_heading": self._find_primary_heading(image_bbox, document_elements),
            "heading_hierarchy": self._get_heading_path(image_bbox, document_elements),
            "surrounding_paragraphs": self._extract_surrounding_text(image_bbox, document_elements),
            "caption": self._find_caption(image_bbox, document_elements),
            "related_tables": self._find_related_tables(image_bbox, document_elements),
            "figure_references": self._detect_figure_references(image_bbox, document_elements),
            "spatial_confidence": self._calculate_confidence(image_bbox, document_elements)
        }

    def _find_primary_heading(self, img_bbox, elements) -> Optional[Dict]:
        headings = [e for e in elements if e.get("type") == "heading"]
        if not headings:
            return None

        scored_headings = []
        for heading in headings:
            y_distance = abs(img_bbox.y0 - heading["bbox"][3])  # vertical distance
            x_overlap = max(0, min(img_bbox.x1, heading["bbox"][2]) - max(img_bbox.x0, heading["bbox"][0]))
            alignment_bonus = x_overlap / max(img_bbox.width, heading["bbox"][2] - heading["bbox"][0])
            level_bonus = max(0, 4 - heading.get("level", 3)) * 10
            score = y_distance - (alignment_bonus * 50) - level_bonus
            scored_headings.append((heading, score))
        best_heading = min(scored_headings, key=lambda x: x[1])[0]
        return best_heading

    # Placeholder implementations below — you will implement the following:

    def _get_heading_path(self, img_bbox, elements) -> List[str]:
        return []

    def _extract_surrounding_text(self, img_bbox, elements) -> List[str]:
        return []

    def _find_caption(self, img_bbox, elements) -> Optional[str]:
        return None

    def _find_related_tables(self, img_bbox, elements) -> List[Dict]:
        return []

    def _detect_figure_references(self, img_bbox, elements) -> List[str]:
        return []

    def _calculate_confidence(self, img_bbox, elements) -> float:
        return 1.0
