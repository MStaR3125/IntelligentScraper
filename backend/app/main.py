import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import asyncio
import json
from datetime import datetime
from typing import List

from database import get_db, ScrapingJob, ScrapedItem
from models import *
from scraper import EnhancedAIWebScraper

app = FastAPI(title="AI Web Scraper", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def send_progress(self, job_id: int, status: str, progress: int, message: str):
        progress_data = {
            "job_id": job_id,
            "status": status,
            "progress": progress,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        # Send to all connected clients
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(progress_data))
            except:
                self.disconnect(connection)

manager = ConnectionManager()
scraper = EnhancedAIWebScraper()

# Scraping routes
@app.post("/api/scraping/start", response_model=ScrapingJobResponse)
async def start_scraping(
    request: ScrapingRequest,
    db: Session = Depends(get_db)
):
    # Create new scraping job
    job = ScrapingJob(
        query=request.query,
        max_results=request.max_results
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    # Start scraping in background
    asyncio.create_task(
        scraper.scrape_with_progress(
            job.id, 
            request.query, 
            request.max_results,
            manager.send_progress
        )
    )
    
    return ScrapingJobResponse(
        id=job.id,
        query=job.query,
        status=job.status,
        max_results=job.max_results,
        created_at=job.created_at,
        completed_at=job.completed_at,
        results_count=job.results_count,
        results_file=job.results_file,
        error_message=job.error_message
    )

@app.get("/api/scraping/jobs", response_model=List[ScrapingJobResponse])
async def get_user_jobs(
    db: Session = Depends(get_db)
):
    jobs = db.query(ScrapingJob).order_by(ScrapingJob.created_at.desc()).all()
    
    result = []
    for job in jobs:
        scraped_items = [
            ScrapedItemResponse(
                id=item.id,
                title=item.title,
                description=item.description,
                url=item.url,
                price=item.price,
                rating=item.rating,
                date=item.date,
                additional_data=json.loads(item.additional_data) if item.additional_data else {}
            )
            for item in job.scraped_items
        ]
        
        result.append(ScrapingJobResponse(
            id=job.id,
            query=job.query,
            status=job.status,
            max_results=job.max_results,
            created_at=job.created_at,
            completed_at=job.completed_at,
            results_count=job.results_count,
            results_file=job.results_file,
            error_message=job.error_message,
            scraped_items=scraped_items
        ))
    
    return result

@app.get("/api/scraping/jobs/{job_id}", response_model=ScrapingJobResponse)
async def get_job_details(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    scraped_items = [
        ScrapedItemResponse(
            id=item.id,
            title=item.title,
            description=item.description,
            url=item.url,
            price=item.price,
            rating=item.rating,
            date=item.date,
            additional_data=json.loads(item.additional_data) if item.additional_data else {}
        )
        for item in job.scraped_items
    ]
    
    return ScrapingJobResponse(
        id=job.id,
        query=job.query,
        status=job.status,
        max_results=job.max_results,
        created_at=job.created_at,
        completed_at=job.completed_at,
        results_count=job.results_count,
        results_file=job.results_file,
        error_message=job.error_message,
        scraped_items=scraped_items
    )

# Export endpoints for CSV and Excel
@app.get("/api/scraping/jobs/{job_id}/export/csv")
async def export_job_csv(job_id: int, db: Session = Depends(get_db)):
    """Export scraping job results as CSV"""
    import pandas as pd
    from fastapi.responses import StreamingResponse
    import io
    
    job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Prepare data for CSV
    data = []
    for item in job.scraped_items:
        additional_data = json.loads(item.additional_data) if item.additional_data else {}
        row = {
            'Title': item.title or '',
            'Description': item.description or '',
            'URL': item.url or '',
            'Price': item.price or '',
            'Rating': item.rating or '',
            'Date': item.date or '',
            **additional_data  # Include additional data as separate columns
        }
        data.append(row)
    
    if not data:
        raise HTTPException(status_code=404, detail="No data found for this job")
    
    # Create DataFrame and CSV
    df = pd.DataFrame(data)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8')
    csv_content = csv_buffer.getvalue()
    
    # Create response
    response = StreamingResponse(
        io.StringIO(csv_content),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=scraping_job_{job_id}_{job.query.replace(' ', '_')}.csv"}
    )
    return response

@app.get("/api/scraping/jobs/{job_id}/export/excel")
async def export_job_excel(job_id: int, db: Session = Depends(get_db)):
    """Export scraping job results as Excel"""
    import pandas as pd
    from fastapi.responses import StreamingResponse
    import io
    
    job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Prepare data for Excel
    data = []
    for item in job.scraped_items:
        additional_data = json.loads(item.additional_data) if item.additional_data else {}
        row = {
            'Title': item.title or '',
            'Description': item.description or '',
            'URL': item.url or '',
            'Price': item.price or '',
            'Rating': item.rating or '',
            'Date': item.date or '',
            **additional_data  # Include additional data as separate columns
        }
        data.append(row)
    
    if not data:
        raise HTTPException(status_code=404, detail="No data found for this job")
    
    # Create DataFrame and Excel
    df = pd.DataFrame(data)
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Scraped Data', index=False)
        
        # Add job information as a second sheet
        job_info = pd.DataFrame([{
            'Job ID': job.id,
            'Query': job.query,
            'Status': job.status,
            'Max Results': job.max_results,
            'Created At': job.created_at,
            'Completed At': job.completed_at,
            'Results Count': job.results_count,
            'Error Message': job.error_message or ''
        }])
        job_info.to_excel(writer, sheet_name='Job Info', index=False)
    
    excel_buffer.seek(0)
    
    # Create response
    response = StreamingResponse(
        io.BytesIO(excel_buffer.read()),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=scraping_job_{job_id}_{job.query.replace(' ', '_')}.xlsx"}
    )
    return response

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def root():
    return {"message": "AI Web Scraper API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)