from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import requests

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Load legal reporters data
REPORTERS_FILE = ROOT_DIR.parent / 'legal_reporters_comprehensive.json'
with open(REPORTERS_FILE, 'r') as f:
    LEGAL_REPORTERS = json.load(f)

# Create lookup dictionaries for fast matching
REPORTER_LOOKUP = {}
for reporter in LEGAL_REPORTERS:
    # Add main abbreviation
    REPORTER_LOOKUP[reporter['abbreviation'].lower()] = reporter
    # Add aliases
    for alias in reporter['aliases']:
        REPORTER_LOOKUP[alias.lower()] = reporter

# Create the main app without a prefix
app = FastAPI(title="Strike Cite API", description="U.S. Legal Citation Validator")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Models for Strike Cite
class CitationElement(BaseModel):
    citation: str
    normalized_citations: List[str] = []
    start_index: int
    end_index: int
    status: int
    error_message: str = ""
    clusters: List[Dict[str, Any]] = []

class ValidatedCitation(BaseModel):
    raw: str
    normalized: str
    reporter: Optional[str]
    verified: bool
    source_url: Optional[str]
    note: str
    start_char: int
    end_char: int

class ValidationSummary(BaseModel):
    total: int
    verified: int
    unverified: int
    confidence: str

class ValidationResult(BaseModel):
    citations: List[ValidatedCitation]
    summary: ValidationSummary

class TextValidationRequest(BaseModel):
    text: str

# Layer A: Core Validation Microservice
def validate_citations(lookup_json: List[Dict[str, Any]]) -> ValidationResult:
    """
    Core validation function that processes LOOKUP_JSON and returns validated citations.
    This is the reusable microservice that can be called by other projects.
    """
    validated_citations = []
    
    for element in lookup_json:
        # 1. Normalize citation
        if element.get('normalized_citations') and len(element['normalized_citations']) > 0:
            normalized = element['normalized_citations'][0]
        else:
            normalized = element.get('citation', '')
        
        # 2. Identify reporter
        reporter_abbrev = None
        citation_text = normalized or element.get('citation', '')
        
        # Extract reporter abbreviation from citation
        # Common patterns: "123 F.3d 456", "410 U.S. 113", etc.
        parts = citation_text.split()
        if len(parts) >= 2:
            potential_reporter = parts[1].lower()
            if potential_reporter in REPORTER_LOOKUP:
                reporter_abbrev = REPORTER_LOOKUP[potential_reporter]['abbreviation']
        
        # 3. Verification status
        verified = element.get('status') == 200
        
        # 4. Source URL
        source_url = None
        if verified and element.get('clusters') and len(element['clusters']) > 0:
            source_url = element['clusters'][0].get('url')
        
        # 5. Generate note for unverified citations
        note = ""
        if not verified:
            if reporter_abbrev is None:
                note = "reporter not recognized"
            elif element.get('status') == 404:
                note = "not found in CourtListener"
            else:
                note = f"status {element.get('status', 'unknown')}"
            
            # Check for common mistakes
            if reporter_abbrev is None and len(parts) >= 2:
                potential_mistakes = parts[1]
                for reporter in LEGAL_REPORTERS:
                    for mistake in reporter.get('common_citation_mistakes', []):
                        if potential_mistakes.lower() in mistake.lower():
                            note = f"possible typo: {mistake[:15]}..."
                            break
        
        validated_citation = ValidatedCitation(
            raw=element.get('citation', ''),
            normalized=normalized,
            reporter=reporter_abbrev,
            verified=verified,
            source_url=source_url,
            note=note,
            start_char=element.get('start_index', 0),
            end_char=element.get('end_index', 0)
        )
        validated_citations.append(validated_citation)
    
    # Calculate summary
    total = len(validated_citations)
    verified_count = sum(1 for c in validated_citations if c.verified)
    unverified_count = total - verified_count
    
    if total == 0:
        confidence = "low"
    elif verified_count / total >= 0.9:
        confidence = "high"
    elif verified_count / total >= 0.6:
        confidence = "medium"
    else:
        confidence = "low"
    
    summary = ValidationSummary(
        total=total,
        verified=verified_count,
        unverified=unverified_count,
        confidence=confidence
    )
    
    return ValidationResult(citations=validated_citations, summary=summary)

# API Endpoints

@api_router.post("/validate-citations", response_model=ValidationResult)
async def validate_citations_endpoint(lookup_json: List[CitationElement]):
    """
    Layer A: Core validation microservice endpoint.
    Takes LOOKUP_JSON from CourtListener and returns validated citations.
    """
    try:
        # Convert Pydantic models to dict for processing
        lookup_data = [element.dict() for element in lookup_json]
        result = validate_citations(lookup_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")

@api_router.post("/validate-text", response_model=ValidationResult)
async def validate_text_endpoint(request: TextValidationRequest):
    """
    Layer B: Full pipeline endpoint.
    Takes text input, calls CourtListener API, then validates citations.
    """
    try:
        # Step 1: Call CourtListener API
        courtlistener_url = "https://www.courtlistener.com/api/rest/v4/citation-lookup/"
        headers = {
            "Authorization": f"Token {os.environ.get('COURTLISTENER_API_KEY', '')}",
            "Content-Type": "application/json"
        }
        
        payload = {"text": request.text}
        
        response = requests.post(courtlistener_url, json=payload, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"CourtListener API error: {response.text}"
            )
        
        lookup_json = response.json()
        
        # Step 2: Validate citations using Layer A
        result = validate_citations(lookup_json)
        return result
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@api_router.get("/reporters", response_model=List[Dict[str, Any]])
async def get_reporters():
    """Get available legal reporters list."""
    return LEGAL_REPORTERS

@api_router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "reporters_loaded": len(LEGAL_REPORTERS)}

# Legacy endpoints (keep existing functionality)
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

@api_router.get("/")
async def root():
    return {"message": "Strike Cite API - U.S. Legal Citation Validator"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

# Log startup info
@app.on_event("startup")
async def startup_event():
    logger.info(f"Strike Cite API started")
    logger.info(f"Loaded {len(LEGAL_REPORTERS)} legal reporters")
    logger.info(f"Reporter lookup table has {len(REPORTER_LOOKUP)} entries")