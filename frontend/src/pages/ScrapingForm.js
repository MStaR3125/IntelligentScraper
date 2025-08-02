import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Slider,
  LinearProgress,
  Alert,
  Card,
  CardContent
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE = 'http://localhost:8001';

function ScrapingForm() {
  const [query, setQuery] = useState('');
  const [maxResults, setMaxResults] = useState(15);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [progressMessage, setProgressMessage] = useState('');
  const [error, setError] = useState('');
  const [currentJobId, setCurrentJobId] = useState(null);
  
  const navigate = useNavigate();

  // WebSocket connection for real-time updates
  useEffect(() => {
    let ws = null;
    
    if (currentJobId) {
      ws = new WebSocket('ws://localhost:8001/ws');
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.job_id === currentJobId) {
          setProgress(data.progress);
          setProgressMessage(data.message);
          
          if (data.status === 'completed') {
            setLoading(false);
            navigate(`/job/${currentJobId}`);
          } else if (data.status === 'failed') {
            setLoading(false);
            setError(data.message);
          }
        }
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    }
    
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [currentJobId, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    setProgress(0);
    setProgressMessage('Initializing...');

    try {
      const response = await axios.post(
        `${API_BASE}/api/scraping/start`,
        {
          query,
          max_results: maxResults
        }
      );

      setCurrentJobId(response.data.id);
    } catch (err) {
      setLoading(false);
      setError(err.response?.data?.detail || 'Failed to start scraping');
    }
  };

  const exampleQueries = [
    "best laptops under $1000 2025",
    "top restaurants in New York City",
    "iPhone 15 prices comparison",
    "Tesla Model 3 reviews and ratings",
    "best coffee shops in San Francisco"
  ];

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom align="center">
          🔍 AI Web Scraper
        </Typography>
        
        <Typography variant="body1" color="text.secondary" align="center" sx={{ mb: 4 }}>
          Enter what you want to scrape and let AI do the work! 
          <br />
          <strong>Note:</strong> The AI agent may take 30-60 seconds to complete scraping. Please be patient! 🤖
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="What do you want to scrape?"
            placeholder="e.g., best pizza places in Chicago, iPhone prices, job listings"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={loading}
            multiline
            rows={3}
            sx={{ mb: 3 }}
            required
          />

          <Box sx={{ mb: 3 }}>
            <Typography gutterBottom>
              Maximum Results: {maxResults}
            </Typography>
            <Slider
              value={maxResults}
              onChange={(e, newValue) => setMaxResults(newValue)}
              min={5}
              max={50}
              step={5}
              marks
              disabled={loading}
            />
          </Box>

          {loading && (
            <Box sx={{ mb: 3 }}>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                {progressMessage}
              </Typography>
              <LinearProgress variant="determinate" value={progress} />
              <Typography variant="caption" sx={{ mt: 1, display: 'block' }}>
                {progress}% Complete
              </Typography>
            </Box>
          )}

          <Button
            type="submit"
            variant="contained"
            size="large"
            fullWidth
            disabled={loading || !query.trim()}
            sx={{ mb: 4 }}
          >
            {loading ? 'Scraping...' : 'Start Scraping'}
          </Button>
        </Box>

        <Typography variant="h6" gutterBottom>
          💡 Example Queries
        </Typography>
        
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {exampleQueries.map((example, index) => (
            <Card
              key={index}
              sx={{ 
                cursor: 'pointer', 
                transition: 'all 0.2s',
                '&:hover': { 
                  backgroundColor: 'action.hover',
                  transform: 'translateY(-2px)'
                }
              }}
              onClick={() => !loading && setQuery(example)}
            >
              <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                <Typography variant="body2">
                  {example}
                </Typography>
              </CardContent>
            </Card>
          ))}
        </Box>
      </Paper>
    </Container>
  );
}

export default ScrapingForm;
