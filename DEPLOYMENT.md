# Deployment Guide for Data Analyst Agent

## Required Files for Deployment

Before deploying, ensure you have these essential files:

### Core Application Files
- **`main.py`** - Your FastAPI application (630+ lines)
- **`requirements.txt`** - Python dependencies
- **`question.txt`** - Sample evaluation question

### Configuration Files
- **`runtime.txt`** - Specifies Python version (Python-3.11.0)
- **`Procfile`** - For Heroku deployment
- **`Dockerfile`** - For container-based deployments
- **`.gitignore`** - Excludes unnecessary files from Git

### Documentation Files (Optional but Recommended)
- **`README.md`** - Project overview and usage
- **`DEPLOYMENT.md`** - This deployment guide

### Testing Files (Optional)
- **`evaluate_agent.py`** - Local evaluation script
- **`test_agent.py`** - API testing script

## GitHub Repository Setup

### Step 1: Create GitHub Repository

1. **Go to GitHub**: Visit https://github.com
2. **Create new repository**:
   - Click the "+" icon → "New repository"
   - Repository name: `data-analyst-agent` or `tds-project2`
   - Description: "TDS Project 2 - Data Analyst Agent API"
   - Make it **Public** (required for free Render tier)
   - Initialize with README: ✅ (if starting fresh)

### Step 2: Upload Files to GitHub

From your project directory, run these commands:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Data Analyst Agent API"

# Add GitHub remote (replace with your repository URL)
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify Upload

Make sure these files are visible on GitHub:
- ✅ main.py
- ✅ requirements.txt  
- ✅ question.txt
- ✅ runtime.txt
- ✅ README.md
- ✅ .gitignore

## Quick Deploy Options

### 1. Heroku (Recommended)

1. **Create Heroku Account** at https://heroku.com

2. **Install Heroku CLI** and login:
```bash
heroku login
```

3. **Deploy from your project directory**:
```bash
git init
git add .
git commit -m "Initial commit"
heroku create your-app-name
git push heroku main
```

4. **Your API will be available at**: `https://your-app-name.herokuapp.com/api/`

### 2. Railway

1. **Visit** https://railway.app
2. **Connect GitHub** and select this repository
3. **Deploy automatically** - Railway will detect the Python app
4. **Get your URL** from the Railway dashboard

### 3. Render (Detailed Steps)

**Step 1: Prepare GitHub Repository**

1. **Create GitHub repository**:
   - Go to https://github.com and create a new repository
   - Name it something like `data-analyst-agent` or `tds-project2`
   - Make it public (required for free Render tier)

2. **Upload these essential files to GitHub**:
   ```
   main.py                 # Your FastAPI application
   requirements.txt        # Python dependencies
   runtime.txt            # Python version (optional)
   README.md              # Project documentation
   question.txt           # Sample question file
   Dockerfile             # Container configuration (optional)
   .gitignore             # Git ignore rules
   ```

3. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy data analyst agent"
   git push origin main
   ```

**Step 2: Deploy on Render**

1. **Visit** https://render.com and sign up/login
2. **Connect GitHub**: Link your GitHub account
3. **Create new Web Service**:
   - Click "New" → "Web Service"
   - Select "Build and deploy from a Git repository"
   - Choose your repository

4. **Configure deployment settings**:
   - **Name**: `data-analyst-agent` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Instance Type**: Free tier (sufficient for testing)

5. **Advanced Settings**:
   - **Port**: Leave empty (auto-detected from main.py)
   - **Environment Variables**: None required (add OPENAI_API_KEY if needed)
   - **Health Check Path**: `/` (your health endpoint)

6. **Deploy**: Click "Create Web Service"

**Step 3: Get Your URL**
- Render will provide a URL like: `https://your-app-name.onrender.com`
- Your API endpoint will be: `https://your-app-name.onrender.com/api/`

### 4. Google Cloud Run

1. **Build and push Docker image**:
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/data-analyst-agent
```

2. **Deploy to Cloud Run**:
```bash
gcloud run deploy --image gcr.io/PROJECT-ID/data-analyst-agent --platform managed
```

### 5. AWS (using Docker)

1. **Push to ECR**:
```bash
aws ecr create-repository --repository-name data-analyst-agent
docker build -t data-analyst-agent .
docker tag data-analyst-agent:latest YOUR-ECR-URI
docker push YOUR-ECR-URI
```

2. **Deploy using ECS/Fargate** or **Lambda**

## Testing Your Deployment

Once deployed, test your API with either method:

**Method 1: File Upload (Original)**
```bash
# Replace YOUR-DOMAIN with your actual domain
curl -X POST "https://YOUR-DOMAIN/api/" -F "file=@question.txt"
```

**Method 2: Direct Text (Compatible with eval system)**
```bash
# Replace YOUR-DOMAIN with your actual domain
curl -X POST "https://YOUR-DOMAIN/api/" \
  -H "Content-Type: text/plain" \
  -d "Scrape the list of highest grossing films from Wikipedia. Answer: 1. How many $2 bn movies were released before 2020? 2. Which is the earliest film that grossed over $1.5 bn? 3. What's the correlation between the Rank and Peak? 4. Draw a scatterplot with red dotted regression line."
```

**Expected Response Format:**
```json
[1, "Titanic", 0.485782, "data:image/png;base64,iVBORw0KG..."]
```

## Environment Variables (Optional)

- `PORT`: Server port (auto-detected on most platforms)
- `OPENAI_API_KEY`: For advanced LLM features

## Performance Notes

- **Memory**: Allocate at least 512MB RAM
- **Timeout**: Set to 300 seconds (5 minutes) for large datasets
- **Concurrent Requests**: The app handles multiple requests efficiently

## Cost Estimates

- **Heroku**: ~$7/month (Hobby tier)
- **Railway**: ~$5/month (Starter tier)  
- **Render**: Free tier available, $7/month for production
- **Google Cloud Run**: Pay per use, very cost-effective for low traffic
- **AWS**: Variable, typically $10-50/month depending on usage
