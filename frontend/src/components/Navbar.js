import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography 
          variant="h6" 
          sx={{ flexGrow: 1, cursor: 'pointer' }}
          onClick={() => navigate('/dashboard')}
        >
          🔍 AI Web Scraper
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button 
            color="inherit" 
            onClick={() => navigate('/dashboard')}
          >
            Dashboard
          </Button>
          
          <Button 
            color="inherit" 
            onClick={() => navigate('/scrape')}
          >
            New Scrape
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
