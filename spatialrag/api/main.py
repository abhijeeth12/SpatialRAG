# spatialrag/api/main.py
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="SpatialRAG API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Your revolutionary RAG system
from spatialrag.core.document_parser import AdvancedDocumentParser
from spatialrag.core.spatial_mapper import SpatialProximityMapper
from spatialrag.core.embedder import JinaV4Embedder

class QueryRequest(BaseModel):
    query: str
    document_ids: List[str]
    include_images: bool = True
    context_radius: int = 150

class SpatialResponse(BaseModel):
    answer: str
    spatial_sources: List[Dict]
    images: List[Dict]
    confidence_score: float

@app.post("/upload")
async def upload_document(file: UploadFile):
    """Upload and process document with spatial intelligence"""
    
    # Your revolutionary processing pipeline
    parser = AdvancedDocumentParser()
    spatial_mapper = SpatialProximityMapper()
    embedder = JinaV4Embedder()
    
    # Parse with spatial awareness
    document_data = parser.parse_document(file.filename)
    
    # Apply spatial mapping (your innovation!)
    spatial_contexts = []
    for element in document_data["spatial_data"]:
        if element["type"] == "image":
            context = spatial_mapper.map_image_to_context(
                element["bbox"], 
                document_data["spatial_data"]
            )
            spatial_contexts.append(context)
    
    return {"document_id": "doc_123", "spatial_contexts": len(spatial_contexts)}

@app.post("/query", response_model=SpatialResponse)
async def query_spatial_rag(request: QueryRequest):
    """Revolutionary spatial-aware RAG query"""
    
    # Your multi-modal retrieval with spatial intelligence
    # This is where the magic happens!
    
    return SpatialResponse(
        answer="Generated answer with spatial context...",
        spatial_sources=[{"heading": "Method", "confidence": 0.95}],
        images=[{"url": "/img1.jpg", "spatial_context": "Method section"}],
        confidence_score=0.91
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
