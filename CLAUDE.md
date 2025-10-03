# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a keyword recommendation system built with Python and deployed on Vercel. The project provides AI-powered keyword suggestions for marketing and SEO purposes using OpenAI's GPT models.

## Core Architecture

- **Main Application**: `app_v2.py` - Flask web application with Streamlit UI integration
- **Core Engine**: `ai_keyword_recommender.py` - Main AI-powered keyword recommendation logic
- **Legacy Engine**: `keyword_recommender_v2.py` - Alternative recommendation implementation
- **API Layer**: `api/index.py` - Vercel serverless function entry point
- **Configuration**: Environment variables in `.env` for API keys and settings

## Development Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally using start script
./start.sh

# Manual run (alternative)
python app_v2.py
```

### Environment Setup
```bash
# Copy environment template
cp .env.example .env
# Edit .env with your OpenAI API key and other settings
```

## Vercel Deployment Setup

### Environment Variables (Required)
Set these in Vercel Dashboard → Project Settings → Environment Variables:
```
OPENAI_API_KEY=your-actual-openai-api-key
USE_AI=true
```

### Deployment Process
```bash
# Deploy to Vercel
vercel deploy

# Production deployment
vercel --prod
```

### Security Notes
- Never commit `.env` files (already in `.gitignore`)
- Always use Vercel environment variables for production
- Rotate any exposed API keys immediately

## File Structure

- `ai_keyword_recommender.py` - Primary recommendation engine with OpenAI integration
- `app_v2.py` - Main Flask application with web interface
- `keyword_recommender_v2.py` - Secondary recommendation implementation
- `api/index.py` - Vercel serverless function that imports and uses the core modules
- `vercel.json` - Vercel deployment configuration
- `start.sh` - Local development startup script
- `requirements.txt` - Python dependencies

## Development Notes

- The project uses Flask for the web framework with custom HTML templates
- OpenAI GPT models are used for AI-powered keyword generation
- The system supports both local development and serverless deployment on Vercel
- Multiple recommendation engines are available for different use cases
- `api/index.py` serves as the Vercel serverless function entry point and imports modules from parent directory