# Tech Trends Scraper for PREPY AI

## Overview
The Tech Trends Scraper keeps PREPY AI's interview and hackathon questions up-to-date with current industry trends by scraping data from:
- **GitHub Trending** - Latest trending repositories and technologies
- **Hacker News** - Current tech discussions and hot topics
- **Stack Overflow** - Popular frameworks and tags

## Features
✅ Automatic tech trends integration into AI prompts
✅ Caches trends data to avoid excessive scraping
✅ Extracts industry buzzwords and popular frameworks
✅ API endpoints for manual updates and viewing trends

## How It Works

### Automatic Integration
When the backend server starts, the scraper:
1. Loads cached trends (if available)
2. Integrates trends into AI system prompts
3. Makes questions more relevant to current tech landscape

### Data Sources
1. **GitHub Trending** - Top 10 trending repositories with languages
2. **Hacker News** - Top 15 front-page stories
3. **Stack Overflow** - Top 20 popular tags/frameworks

### Cached Data
Trends are cached in `tech_trends_cache.json` to:
- Reduce API calls to external sites
- Provide offline fallback
- Track last update timestamp

## Usage

### Running the Scraper Manually
```bash
cd BACKEND
python tech_trends_scraper.py
```

This will:
- Scrape all three sources
- Display a summary of trends
- Save data to `tech_trends_cache.json`

### API Endpoints

#### Update Trends (Manual Trigger)
```bash
POST http://localhost:5000/api/update-trends
```

Response:
```json
{
  "success": true,
  "message": "Tech trends updated successfully",
  "data": {
    "trending_tech": [...],
    "hot_topics": [...],
    "popular_frameworks": [...],
    "buzzwords": [...],
    "last_updated": "2025-11-29T04:14:08.365701"
  }
}
```

#### Get Current Trends
```bash
GET http://localhost:5000/api/get-trends
```

Response:
```json
{
  "success": true,
  "data": {
    "trending_tech": [...],
    "hot_topics": [...],
    "popular_frameworks": [...],
    "buzzwords": [...]
  },
  "summary": "CURRENT TECH TRENDS (Last Updated: ...)..."
}
```

## How It Improves Interviews

### Before (Generic Questions)
❌ "What technologies did you use?"
❌ "How does it work?"

### After (Trend-Aware Questions)
✅ "Did you use React or Next.js?" (if trending)
✅ "How does your AI model compare to GPT-4?" (if AI is trending)
✅ "Did you implement any Rust components?" (if Rust is trending)

## Configuration

### Update Frequency
By default, trends are cached and reused. To update:
1. **Manual**: Call `/api/update-trends` endpoint
2. **Automatic**: Run `python tech_trends_scraper.py` as a cron job

### Customization
Edit `tech_trends_scraper.py` to:
- Add more data sources
- Change number of items scraped
- Modify buzzword extraction logic

## Files Created
- `tech_trends_scraper.py` - Main scraper module
- `tech_trends_cache.json` - Cached trends data (auto-generated)

## Dependencies
```
beautifulsoup4==4.12.2
requests==2.31.0
```

## Example Output
```
🔍 Starting tech trends scraping...
==================================================
✅ Scraped 10 GitHub trending repos
✅ Scraped 15 Hacker News topics
✅ Scraped 20 Stack Overflow tags
✅ Extracted 50 buzzwords
✅ Trends saved to tech_trends_cache.json
==================================================
✅ Successfully updated 3/3 sources

CURRENT TECH TRENDS (Last Updated: 2025-11-29T04:14:08.365701)

📈 TRENDING TECHNOLOGIES:
  • facebook/react (JavaScript)
  • vercel/next.js (JavaScript)
  • microsoft/vscode (TypeScript)
  • rust-lang/rust (Rust)
  • golang/go (Go)

🔥 HOT TOPICS:
  • New AI Model Beats GPT-4
  • Rust in Production at Scale
  • Next.js 15 Released
  ...

🛠️ POPULAR FRAMEWORKS/TAGS:
  • javascript, python, java, react, typescript, node.js, rust, go, docker, kubernetes

💡 INDUSTRY BUZZWORDS:
ai, machine-learning, llm, kubernetes, docker, microservices, serverless, edge-computing...
```

## Best Practices
1. **Update Weekly**: Run scraper once a week for fresh trends
2. **Monitor Cache**: Check `tech_trends_cache.json` last_updated timestamp
3. **Review Questions**: Ensure AI questions align with candidate's domain

## Troubleshooting

### Scraping Fails
- Check internet connection
- Websites may have changed their HTML structure
- Rate limiting (wait and retry)

### Empty Trends
- Delete `tech_trends_cache.json` and re-run
- Check console output for specific errors

### AI Not Using Trends
- Verify trends are loaded: `GET /api/get-trends`
- Check system prompt includes tech_awareness section
- Restart backend server

## Future Enhancements
- [ ] Add more data sources (Reddit, Dev.to, Medium)
- [ ] Implement automatic daily updates
- [ ] Add trend analysis and scoring
- [ ] Create frontend dashboard for trends visualization
- [ ] Add filtering by tech domain (AI/ML, Web Dev, DevOps, etc.)
