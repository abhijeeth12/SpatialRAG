# spatialrag/api/main.py
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any  
import uvicorn
import tempfile
import os

app = FastAPI(title="SpatialRAG API", version="1.0.0")
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Import your revolutionary RAG system
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
    spatial_sources: List[Dict[str, Any]]
    images: List[Dict[str, Any]]
    confidence_score: float

class UploadResponse(BaseModel):
    document_id: str
    filename: str
    spatial_contexts: int
    message: str

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "SpatialRAG API is running! 🚀"}

@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile):
    """Upload and process document with spatial intelligence"""
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Initialize your revolutionary processing pipeline
        parser = AdvancedDocumentParser()
        spatial_mapper = SpatialProximityMapper()
        embedder = JinaV4Embedder()
        
        # Parse with spatial awareness
        document_data = parser.parse_document(tmp_file_path)
        
        # Apply spatial mapping (your innovation!)
        spatial_contexts = []
        for element in document_data["spatial_data"]:
            if element["type"] == "image":
                context = spatial_mapper.map_image_to_context(
                    element["bbox"], 
                    document_data["spatial_data"]
                )
                spatial_contexts.append(context)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        return UploadResponse(
            document_id=f"doc_{hash(file.filename)}",
            filename=file.filename,
            spatial_contexts=len(spatial_contexts),
            message="Document processed with spatial intelligence!"
        )
        
    except Exception as e:
        # Clean up on error
        if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.post("/query", response_model=SpatialResponse)
async def query_spatial_rag(request: QueryRequest):
    """Revolutionary spatial-aware RAG query"""
    
    try:
        # Your multi-modal retrieval with spatial intelligence
        # This is where the magic happens!
        
        # Mock response for now - you'll implement the real logic
        mock_spatial_sources = [
            {
                "heading": "Methodology", 
                "content": "Sample content from methodology section",
                "confidence": 0.95,
                "spatial_context": "Primary heading with nearby image"
            }
        ]
        
        mock_images = [
            {
                "url": "/images/method_diagram.jpg",
                "heading": "Methodology",
                "caption": "Figure 2: Training pipeline overview",
                "spatial_confidence": 0.89
            }
        ]
        
        return SpatialResponse(
            answer="Generated answer with revolutionary spatial context awareness...",
            spatial_sources=mock_spatial_sources,
            images=mock_images,
            confidence_score=0.91
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check for deployment"""
    return {"status": "healthy", "message": "SpatialRAG is ready to revolutionize RAG!"}

if __name__ == "__main__":
    print("🚀 Starting SpatialRAG API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 Docs available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
