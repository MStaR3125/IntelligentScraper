from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ScrapingRequest(BaseModel):
    query: str
    max_results: int = 15

class ScrapedItemResponse(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    url: Optional[str]
    price: Optional[str]
    rating: Optional[str]
    date: Optional[str]
    additional_data: Dict[str, Any] = {}

class ScrapingJobResponse(BaseModel):
    id: int
    query: str
    status: str
    max_results: int
    created_at: datetime
    completed_at: Optional[datetime]
    results_count: int
    results_file: Optional[str]
    error_message: Optional[str]
    scraped_items: List[ScrapedItemResponse] = []

class ScrapingProgress(BaseModel):
    job_id: int
    status: str
    progress: int
    message: str