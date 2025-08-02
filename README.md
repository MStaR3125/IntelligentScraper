# 🔍 AI Web Scraper

A powerful, intelligent web scraping application that combines AI capabilities with a modern web interface. This full-stack application allows users to scrape web data using natural language queries and provides real-time progress tracking, data visualization, and export capabilities.

## 🌟 Features

### 🤖 AI-Powered Scraping
- **Natural Language Queries**: Simply describe what you want to scrape in plain English
- **Intelligent Data Extraction**: Uses Google's Gemini AI model for smart content understanding
- **Browser Automation**: Powered by `browser-use` library for dynamic web interaction
- **Flexible Results**: Extracts titles, descriptions, prices, ratings, URLs, and additional metadata

### 🎯 User-Friendly Interface
- **Modern React Frontend**: Built with Material-UI for a professional, responsive design
- **Real-time Progress Tracking**: WebSocket-powered live updates during scraping
- **Job Management Dashboard**: View all your scraping jobs with status tracking
- **Detailed Results View**: Comprehensive display of scraped data with filtering

### 📊 Data Management
- **Multiple Export Formats**: CSV and Excel export capabilities
- **SQLite Database**: Persistent storage for all scraping jobs and results
- **Job History**: Keep track of all previous scraping operations
- **Error Handling**: Comprehensive error tracking and reporting

### ⚡ Performance & Reliability
- **Asynchronous Processing**: Non-blocking scraping operations
- **FastAPI Backend**: High-performance REST API with automatic documentation
- **Progress Monitoring**: Real-time updates on scraping progress
- **Configurable Limits**: Set maximum results per scraping job (5-50 items)

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework with automatic API documentation
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Uvicorn**: ASGI server implementation
- **WebSockets**: Real-time communication for progress updates
- **Pandas**: Data manipulation and export functionality
- **Google Gemini AI**: Advanced language model for intelligent scraping
- **Browser-Use**: AI-powered browser automation

### Frontend
- **React 18**: Modern JavaScript framework with hooks
- **Material-UI (MUI)**: React component library for professional UI
- **React Router**: Client-side routing for single-page application
- **Axios**: HTTP client for API communication
- **WebSocket Client**: Real-time updates from backend
- **Recharts**: Data visualization library

### Database
- **SQLite**: Lightweight, file-based database
- **Alembic**: Database migration toolkit

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager
- Google API key for Gemini AI

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-web-scraper.git
   cd ai-web-scraper
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   Create a `.env` file in the backend directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   DATABASE_URL=sqlite:///./scraper.db
   ```

4. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. **Start the Backend Server**
   ```bash
   cd backend
   python start_server.py
   ```
   The API will be available at `http://localhost:8001`
   API documentation: `http://localhost:8001/docs`

2. **Start the Frontend Development Server**
   ```bash
   cd frontend
   npm start
   ```
   The web application will be available at `http://localhost:3000`

## 📖 Usage

### Basic Scraping Workflow

1. **Navigate to the Scraping Form** (`/scrape`)
2. **Enter your query** in natural language:
   - "best laptops under $1000 2025"
   - "top restaurants in New York City"
   - "iPhone 15 prices comparison"
3. **Set maximum results** (5-50 items)
4. **Click "Start Scraping"** and watch real-time progress
5. **View results** in the automatically opened job details page
6. **Export data** as CSV or Excel files

### Example Queries
- Product searches: "gaming keyboards under $100"
- Local businesses: "coffee shops in downtown Seattle"
- Price comparisons: "MacBook Pro M3 prices"
- Reviews and ratings: "best streaming services 2025"
- Job listings: "software engineer jobs in San Francisco"

## 🏗️ Project Structure

```
ai-web-scraper/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI application and routes
│   │   ├── database.py       # Database models and connection
│   │   ├── models.py         # Pydantic models for API
│   │   ├── scraper.py        # AI scraping logic
│   │   └── scraper.db        # SQLite database file
│   ├── requirements.txt      # Python dependencies
│   └── start_server.py       # Server startup script
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Navbar.js     # Navigation component
│   │   ├── pages/
│   │   │   ├── Dashboard.js  # Jobs overview page
│   │   │   ├── ScrapingForm.js # Main scraping interface
│   │   │   └── JobDetails.js # Individual job results
│   │   ├── App.js           # Main application component
│   │   └── index.js         # React entry point
│   ├── public/
│   │   └── index.html       # HTML template
│   └── package.json         # Node.js dependencies
└── README.md
```

## 🔧 API Endpoints

### Scraping Operations
- `POST /api/scraping/start` - Start a new scraping job
- `GET /api/scraping/jobs` - List all scraping jobs
- `GET /api/scraping/jobs/{job_id}` - Get specific job details
- `GET /api/scraping/jobs/{job_id}/export/csv` - Export job results as CSV
- `GET /api/scraping/jobs/{job_id}/export/excel` - Export job results as Excel

### WebSocket
- `WS /ws` - Real-time progress updates

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## 🌍 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key | Yes | - |
| `DATABASE_URL` | Database connection string | No | `sqlite:///./scraper.db` |

## 🧪 Development

### Backend Development
```bash
cd backend
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

### Frontend Development
```bash
cd frontend
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## 📄 Database Schema

### ScrapingJob
- `id`: Primary key
- `query`: User's search query
- `status`: Job status (pending, running, completed, failed)
- `max_results`: Maximum number of results to scrape
- `created_at`: Job creation timestamp
- `completed_at`: Job completion timestamp
- `results_count`: Number of items scraped
- `error_message`: Error details if job failed

### ScrapedItem
- `id`: Primary key
- `job_id`: Foreign key to ScrapingJob
- `title`: Item title/name
- `description`: Item description
- `url`: Source URL
- `price`: Price information
- `rating`: Rating/review score
- `date`: Item date
- `additional_data`: JSON field for extra metadata

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Known Issues & Limitations

- AI scraping can take 30-60 seconds depending on query complexity
- Currently supports English language queries primarily
- Rate limited by Google Gemini API quotas
- Some websites may block automated access

## 🔮 Future Enhancements

- [ ] Multi-language support for queries
- [ ] Custom scraping templates
- [ ] Data visualization charts
- [ ] Scheduled/recurring scraping jobs
- [ ] Advanced filtering and search
- [ ] User authentication and multi-tenancy
- [ ] API rate limiting and throttling
- [ ] Support for additional AI models
- [ ] Mobile-responsive improvements
- [ ] Data quality scoring and validation

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/ai-web-scraper/issues) page
2. Create a new issue with detailed description
3. Include error logs and steps to reproduce

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [React](https://reactjs.org/) - Frontend framework
- [Material-UI](https://mui.com/) - React component library
- [Google Gemini](https://ai.google.dev/) - AI model for intelligent scraping
- [Browser-Use](https://github.com/gregpr07/browser-use) - Browser automation library

---

⭐ If you find this project helpful, please give it a star on GitHub!