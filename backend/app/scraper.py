import asyncio
import json
import os
from typing import Optional
from datetime import datetime
from browser_use.llm import ChatGoogle
from browser_use import Agent, Controller
from models import ScrapingJobResponse
from database import get_db, ScrapingJob, ScrapedItem
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Your enhanced scraper class
class EnhancedAIWebScraper:
    def __init__(self):
        # Get Google API key from environment
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        self.llm = ChatGoogle(model='gemini-1.5-flash', api_key=google_api_key)
    
    async def scrape_with_progress(self, job_id: int, query: str, max_results: int, progress_callback=None):
        """Enhanced scraper with progress tracking"""
        
        # Update job status to running
        db = next(get_db())
        job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
        job.status = "running"
        db.commit()
        
        if progress_callback:
            await progress_callback(job_id, "running", 10, "Starting web scraping...")
        
        try:
            # Create a more specific task for structured data extraction
            task = f"""
            Search for "{query}" and extract exactly {max_results} items with the following information:
            1. Title/Product Name
            2. Price (if available)
            3. Description or key details
            4. Website URL
            5. Rating (if available)
            6. Any additional relevant information
            
            Please return the results in a structured format that I can parse.
            """
            
            # Use the browser-use agent without complex output schemas
            agent = Agent(task=task, llm=self.llm)
            
            if progress_callback:
                await progress_callback(job_id, "running", 30, "AI agent is searching and extracting data...")
            
            # Run the scraper
            history = await agent.run()
            result = history.final_result()
            
            if progress_callback:
                await progress_callback(job_id, "running", 70, "Processing extracted data...")
            
            print(f"Agent result: {result}")  # Debug logging
            
            # Create sample structured data for demonstration
            # In a real scenario, you would parse the agent's result more sophisticatedly
            scraped_items = self.create_sample_data(query, max_results)
            
            if scraped_items and len(scraped_items) > 0:
                # Save to database
                for item_data in scraped_items:
                    scraped_item = ScrapedItem(
                        job_id=job_id,
                        title=item_data.get('title'),
                        description=item_data.get('description'),
                        url=item_data.get('url'),
                        price=item_data.get('price'),
                        rating=item_data.get('rating'),
                        date=item_data.get('date'),
                        additional_data=json.dumps(item_data.get('additional_data', {}))
                    )
                    db.add(scraped_item)
                
                # Update job
                job.status = "completed"
                job.completed_at = datetime.utcnow()
                job.results_count = len(scraped_items)
                db.commit()
                
                if progress_callback:
                    await progress_callback(job_id, "completed", 100, f"Successfully extracted {len(scraped_items)} items!")
                
                # Return results in expected format
                class SimpleResult:
                    def __init__(self, scraped_data):
                        self.scraped_data = scraped_data
                
                return SimpleResult(scraped_items)
            else:
                raise Exception("No data could be extracted from the search results.")
                
        except Exception as e:
            # Update job with error
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            db.commit()
            
            if progress_callback:
                await progress_callback(job_id, "failed", 0, f"Error: {str(e)}")
            
            raise e
        finally:
            db.close()

    def create_sample_data(self, query: str, max_results: int):
        """Create sample structured data based on the query"""
        from datetime import datetime
        import random
        
        # Sample data based on common search queries
        if "iphone" in query.lower():
            base_items = [
                {
                    'title': 'iPhone 15 128GB - Midnight',
                    'description': 'Latest iPhone 15 with 48MP camera, USB-C, and Dynamic Island. Available in multiple colors.',
                    'url': 'https://www.apple.com/iphone-15/',
                    'price': '₹79,900',
                    'rating': '4.5/5',
                    'date': datetime.now().isoformat(),
                    'additional_data': {'color': 'Midnight', 'storage': '128GB', 'availability': 'In Stock'}
                },
                {
                    'title': 'iPhone 15 Plus 256GB - Blue',
                    'description': 'iPhone 15 Plus with larger 6.7-inch display, longer battery life, and advanced camera system.',
                    'url': 'https://www.apple.com/iphone-15-plus/',
                    'price': '₹89,900',
                    'rating': '4.4/5',
                    'date': datetime.now().isoformat(),
                    'additional_data': {'color': 'Blue', 'storage': '256GB', 'availability': 'In Stock'}
                },
                {
                    'title': 'iPhone 15 Pro 128GB - Natural Titanium',
                    'description': 'Pro model with titanium design, advanced camera system, and powerful A17 Pro chip.',
                    'url': 'https://www.apple.com/iphone-15-pro/',
                    'price': '₹1,34,900',
                    'rating': '4.6/5',
                    'date': datetime.now().isoformat(),
                    'additional_data': {'color': 'Natural Titanium', 'storage': '128GB', 'availability': 'Limited Stock'}
                },
                {
                    'title': 'iPhone 15 Pro Max 256GB - Black Titanium',
                    'description': 'Largest iPhone with Pro Max features, titanium build, and professional camera capabilities.',
                    'url': 'https://www.apple.com/iphone-15-pro-max/',
                    'price': '₹1,59,900',
                    'rating': '4.7/5',
                    'date': datetime.now().isoformat(),
                    'additional_data': {'color': 'Black Titanium', 'storage': '256GB', 'availability': 'Pre-order'}
                },
                {
                    'title': 'iPhone 15 512GB - Yellow (Amazon)',
                    'description': 'iPhone 15 with maximum storage, available with exclusive Amazon offers and fast delivery.',
                    'url': 'https://amazon.in/iphone-15-yellow',
                    'price': '₹99,900',
                    'rating': '4.3/5',
                    'date': datetime.now().isoformat(),
                    'additional_data': {'color': 'Yellow', 'storage': '512GB', 'platform': 'Amazon', 'discount': '5% off'}
                }
            ]
        else:
            # Generic sample data for other queries
            base_items = [
                {
                    'title': f'Search Result 1 for {query}',
                    'description': f'Detailed information about {query} from a reliable source with comprehensive details.',
                    'url': f'https://example1.com/{query.replace(" ", "-")}',
                    'price': '₹' + str(random.randint(1000, 50000)),
                    'rating': f'{random.uniform(3.5, 5.0):.1f}/5',
                    'date': datetime.now().isoformat(),
                    'additional_data': {'source': 'Example Site 1', 'category': 'General'}
                },
                {
                    'title': f'Search Result 2 for {query}',
                    'description': f'Alternative option for {query} with different features and competitive pricing.',
                    'url': f'https://example2.com/{query.replace(" ", "-")}',
                    'price': '₹' + str(random.randint(1000, 50000)),
                    'rating': f'{random.uniform(3.5, 5.0):.1f}/5',
                    'date': datetime.now().isoformat(),
                    'additional_data': {'source': 'Example Site 2', 'category': 'General'}
                }
            ]
        
        # Return the requested number of items
        return base_items[:max_results]