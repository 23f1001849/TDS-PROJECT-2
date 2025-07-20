# Deployment Guide for Data Analyst Agent

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

### 3. Render

1. **Visit** https://render.com
2. **Create new Web Service** from Git repository
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `python main.py`
5. **Deploy**

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

Once deployed, test your API:

```bash
# Replace YOUR-DOMAIN with your actual domain
curl -X POST "https://YOUR-DOMAIN/api/" -F "file=@question.txt"
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
