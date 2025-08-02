import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Grid,
  Chip,
  Button,
  LinearProgress,
  Alert,
  Link,
  Divider
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE = 'http://localhost:8001';

function JobDetails() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchJobDetails();
  }, [jobId]);

  const fetchJobDetails = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/scraping/jobs/${jobId}`);
      setJob(response.data);
    } catch (err) {
      setError('Failed to fetch job details');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'success';
      case 'running': return 'warning';
      case 'failed': return 'error';
      default: return 'default';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  const handleExportCSV = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/scraping/jobs/${jobId}/export/csv`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `scraping_job_${jobId}_${job.query.replace(/\s+/g, '_')}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to export CSV');
    }
  };

  const handleExportExcel = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/scraping/jobs/${jobId}/export/excel`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `scraping_job_${jobId}_${job.query.replace(/\s+/g, '_')}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to export Excel');
    }
  };

  if (loading) return <LinearProgress />;

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  if (!job) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="warning">Job not found</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4">
          Job Details
        </Typography>
        <Button 
          variant="outlined" 
          onClick={() => navigate('/dashboard')}
        >
          ← Back to Dashboard
        </Button>
      </Box>

      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 3 }}>
            <Typography variant="h5" sx={{ flexGrow: 1, mr: 2 }}>
              {job.query}
            </Typography>
            <Chip 
              label={job.status} 
              color={getStatusColor(job.status)}
              size="large"
            />
          </Box>

          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                Created
              </Typography>
              <Typography variant="body1">
                {formatDate(job.created_at)}
              </Typography>
            </Grid>
            
            {job.completed_at && (
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="body2" color="text.secondary">
                  Completed
                </Typography>
                <Typography variant="body1">
                  {formatDate(job.completed_at)}
                </Typography>
              </Grid>
            )}
            
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                Results Found
              </Typography>
              <Typography variant="body1">
                {job.results_count} / {job.max_results}
              </Typography>
            </Grid>
            
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                Job ID
              </Typography>
              <Typography variant="body1">
                #{job.id}
              </Typography>
            </Grid>
          </Grid>

          {job.error_message && (
            <Alert severity="error" sx={{ mb: 3 }}>
              <Typography variant="body2">
                <strong>Error:</strong> {job.error_message}
              </Typography>
            </Alert>
          )}
        </CardContent>
      </Card>

      {job.scraped_items && job.scraped_items.length > 0 && (
        <Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h5">
              Scraped Results ({job.scraped_items.length})
            </Typography>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button 
                variant="outlined" 
                onClick={handleExportCSV}
                size="small"
                sx={{ minWidth: 'auto' }}
              >
                📄 Export CSV
              </Button>
              <Button 
                variant="outlined" 
                onClick={handleExportExcel}
                size="small"
                sx={{ minWidth: 'auto' }}
              >
                📊 Export Excel
              </Button>
            </Box>
          </Box>
          
          <Grid container spacing={3}>
            {job.scraped_items.map((item, index) => (
              <Grid item xs={12} md={6} lg={4} key={item.id}>
                <Card sx={{ height: '100%' }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom sx={{ 
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical'
                    }}>
                      {item.title || `Item ${index + 1}`}
                    </Typography>
                    
                    {item.description && (
                      <Typography variant="body2" color="text.secondary" sx={{ 
                        mb: 2,
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        display: '-webkit-box',
                        WebkitLineClamp: 3,
                        WebkitBoxOrient: 'vertical'
                      }}>
                        {item.description}
                      </Typography>
                    )}
                    
                    <Box sx={{ mb: 2 }}>
                      {item.price && (
                        <Chip 
                          label={`💰 ${item.price}`} 
                          variant="outlined" 
                          size="small" 
                          sx={{ mr: 1, mb: 1 }}
                        />
                      )}
                      
                      {item.rating && (
                        <Chip 
                          label={`⭐ ${item.rating}`} 
                          variant="outlined" 
                          size="small" 
                          sx={{ mr: 1, mb: 1 }}
                        />
                      )}
                      
                      {item.date && (
                        <Chip 
                          label={`📅 ${item.date}`} 
                          variant="outlined" 
                          size="small" 
                          sx={{ mr: 1, mb: 1 }}
                        />
                      )}
                    </Box>
                    
                    {item.url && (
                      <Link 
                        href={item.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        sx={{ 
                          display: 'block',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap'
                        }}
                      >
                        View Source →
                      </Link>
                    )}
                    
                    {Object.keys(item.additional_data || {}).length > 0 && (
                      <Box sx={{ mt: 2 }}>
                        <Divider sx={{ mb: 1 }} />
                        <Typography variant="caption" color="text.secondary">
                          Additional Data:
                        </Typography>
                        {Object.entries(item.additional_data).map(([key, value]) => (
                          <Typography key={key} variant="caption" display="block">
                            <strong>{key}:</strong> {String(value)}
                          </Typography>
                        ))}
                      </Box>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {job.status === 'completed' && (!job.scraped_items || job.scraped_items.length === 0) && (
        <Alert severity="info">
          No results were found for this scraping job.
        </Alert>
      )}
    </Container>
  );
}

export default JobDetails;
