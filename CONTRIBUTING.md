# Contributing to AI Web Scraper

Thank you for your interest in contributing to AI Web Scraper! This document provides guidelines for contributing to the project.

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code:
- Be respectful and inclusive
- Use welcoming and inclusive language
- Be collaborative
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots if possible**
- **Include your environment details** (OS, Python version, Node.js version, browser)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain which behavior you expected to see instead**
- **Explain why this enhancement would be useful**
- **List some other applications where this enhancement exists**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **If you've added code that should be tested**, add tests
3. **If you've changed APIs**, update the documentation
4. **Ensure the test suite passes**
5. **Make sure your code lints**
6. **Issue that pull request**

### Development Setup

1. Fork and clone the repository
2. Follow the installation instructions in the README
3. Create a new branch for your feature or bug fix
4. Make your changes
5. Test your changes thoroughly
6. Commit your changes with a clear commit message
7. Push to your fork and submit a pull request

### Development Guidelines

#### Backend (Python)
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Add unit tests for new functionality
- Use meaningful variable and function names

#### Frontend (React)
- Follow React best practices
- Use functional components with hooks
- Write clean, readable JSX
- Use Material-UI components consistently
- Add PropTypes or TypeScript types

#### Commit Messages
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Testing

- Write tests for new features
- Ensure all tests pass before submitting a pull request
- Include both unit tests and integration tests where appropriate

### Documentation

- Update the README.md if you change functionality
- Comment your code where necessary
- Update API documentation for any API changes

## Development Environment

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## Project Structure

Please maintain the existing project structure:
- Backend API code in `backend/app/`
- Frontend React code in `frontend/src/`
- Documentation in the root directory
- Tests alongside their respective code

## Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. Tag the release

## Questions?

If you have questions about contributing, please create an issue with the "question" label or reach out to the maintainers.

Thank you for contributing! 🎉
