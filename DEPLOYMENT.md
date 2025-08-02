# Deployment Guide - WhatsApp Group Link Scraper API

## Option 1: Deploy to Railway (Recommended - Free)

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"

### Step 2: Deploy from GitHub
1. Choose "Deploy from GitHub repo"
2. Select your repository
3. Railway will automatically detect it's a Python app
4. Click "Deploy"

### Step 3: Get Your Public URL
1. Once deployed, Railway will give you a public URL like: `https://your-app-name.railway.app`
2. Your API will be accessible at:
   - Main page: `https://your-app-name.railway.app/`
   - API endpoint: `https://your-app-name.railway.app/scrape`
   - Health check: `https://your-app-name.railway.app/health`

## Option 2: Deploy to Render (Free Tier)

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" and select "Web Service"

### Step 2: Connect Repository
1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn main:app`
4. Click "Create Web Service"

## Option 3: Deploy to Heroku (Paid)

### Step 1: Install Heroku CLI
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Deploy
```bash
heroku create your-app-name
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## Environment Variables (Optional)

For production, you may want to set these environment variables:
- `PROXY_USERNAME`: Your proxy username
- `PROXY_PASSWORD`: Your proxy password
- `PROXY_IP`: Your proxy IP
- `PROXY_PORT_START`: Starting port (default: 10000)
- `PROXY_PORT_END`: Ending port (default: 10100)

## Testing Your Deployed API

Once deployed, test with:
```bash
curl -X POST https://your-app-url.com/scrape \
  -H "Content-Type: application/json" \
  -d '{"link": "https://chat.whatsapp.com/XXXXXXXXX"}'
```

## API Endpoints

- `GET /` - Main page with testing interface
- `GET /docs` - API documentation
- `GET /health` - Health check
- `POST /scrape` - Scrape WhatsApp group metadata
- `POST /test-scrape` - Test scraping with form data 