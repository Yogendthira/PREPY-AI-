import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

class TechTrendsScraper:
    """
    Scrapes latest tech trends from multiple sources to keep interview questions current.
    """
    
    def __init__(self):
        self.trends_file = 'tech_trends_cache.json'
        self.trends_data = self.load_cached_trends()
    
    def load_cached_trends(self):
        """Load previously cached trends"""
        if os.path.exists(self.trends_file):
            try:
                with open(self.trends_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading cached trends: {e}")
        return {
            'last_updated': None,
            'trending_technologies': [],
            'hot_topics': [],
            'popular_frameworks': [],
            'industry_buzzwords': []
        }
    
    def save_trends(self):
        """Save trends to cache file"""
        try:
            with open(self.trends_file, 'w', encoding='utf-8') as f:
                json.dump(self.trends_data, f, indent=2)
            print(f"✅ Trends saved to {self.trends_file}")
        except Exception as e:
            print(f"Error saving trends: {e}")
    
    def scrape_github_trending(self):
        """Scrape GitHub trending repositories"""
        try:
            url = 'https://github.com/trending'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                repos = soup.find_all('article', class_='Box-row')
                
                trending_tech = []
                for repo in repos[:10]:  # Top 10
                    try:
                        name = repo.find('h2').get_text(strip=True)
                        desc = repo.find('p', class_='col-9')
                        description = desc.get_text(strip=True) if desc else ''
                        
                        # Extract language
                        lang_span = repo.find('span', itemprop='programmingLanguage')
                        language = lang_span.get_text(strip=True) if lang_span else 'Unknown'
                        
                        trending_tech.append({
                            'name': name,
                            'description': description,
                            'language': language
                        })
                    except Exception as e:
                        continue
                
                self.trends_data['trending_technologies'] = trending_tech
                print(f"✅ Scraped {len(trending_tech)} GitHub trending repos")
                return True
        except Exception as e:
            print(f"❌ GitHub scraping error: {e}")
        return False
    
    def scrape_hackernews(self):
        """Scrape Hacker News front page for tech topics"""
        try:
            url = 'https://news.ycombinator.com/'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                stories = soup.find_all('span', class_='titleline')
                
                hot_topics = []
                for story in stories[:15]:  # Top 15
                    try:
                        link = story.find('a')
                        if link:
                            title = link.get_text(strip=True)
                            hot_topics.append(title)
                    except Exception as e:
                        continue
                
                self.trends_data['hot_topics'] = hot_topics
                print(f"✅ Scraped {len(hot_topics)} Hacker News topics")
                return True
        except Exception as e:
            print(f"❌ Hacker News scraping error: {e}")
        return False
    
    def scrape_stackoverflow_tags(self):
        """Scrape Stack Overflow trending tags"""
        try:
            url = 'https://stackoverflow.com/tags'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                tags = soup.find_all('div', class_='s-card')
                
                popular_frameworks = []
                for tag in tags[:20]:  # Top 20
                    try:
                        tag_name = tag.find('a', class_='post-tag')
                        if tag_name:
                            popular_frameworks.append(tag_name.get_text(strip=True))
                    except Exception as e:
                        continue
                
                self.trends_data['popular_frameworks'] = popular_frameworks
                print(f"✅ Scraped {len(popular_frameworks)} Stack Overflow tags")
                return True
        except Exception as e:
            print(f"❌ Stack Overflow scraping error: {e}")
        return False
    
    def extract_industry_buzzwords(self):
        """Extract key buzzwords from all scraped data"""
        buzzwords = set()
        
        # From GitHub trending
        for tech in self.trends_data.get('trending_technologies', []):
            words = tech['name'].split('/')[-1].split('-')
            buzzwords.update([w.lower() for w in words if len(w) > 3])
            
            if tech['language']:
                buzzwords.add(tech['language'].lower())
        
        # From Hacker News
        for topic in self.trends_data.get('hot_topics', []):
            # Extract tech-related words (simple heuristic)
            words = topic.split()
            for word in words:
                if len(word) > 4 and word[0].isupper():
                    buzzwords.add(word)
        
        # From Stack Overflow
        buzzwords.update(self.trends_data.get('popular_frameworks', []))
        
        self.trends_data['industry_buzzwords'] = list(buzzwords)[:50]  # Top 50
        print(f"✅ Extracted {len(self.trends_data['industry_buzzwords'])} buzzwords")
    
    def update_all_trends(self):
        """Scrape all sources and update trends"""
        print("\n🔍 Starting tech trends scraping...")
        print("=" * 50)
        
        success_count = 0
        
        if self.scrape_github_trending():
            success_count += 1
        
        if self.scrape_hackernews():
            success_count += 1
        
        if self.scrape_stackoverflow_tags():
            success_count += 1
        
        if success_count > 0:
            self.extract_industry_buzzwords()
            self.trends_data['last_updated'] = datetime.now().isoformat()
            self.save_trends()
            print("=" * 50)
            print(f"✅ Successfully updated {success_count}/3 sources")
            return True
        else:
            print("=" * 50)
            print("❌ Failed to update trends from any source")
            return False
    
    def get_trends_summary(self):
        """Get a formatted summary of current trends"""
        summary = f"""
CURRENT TECH TRENDS (Last Updated: {self.trends_data.get('last_updated', 'Never')})

📈 TRENDING TECHNOLOGIES:
{chr(10).join([f"  • {t['name']} ({t['language']})" for t in self.trends_data.get('trending_technologies', [])[:5]])}

🔥 HOT TOPICS:
{chr(10).join([f"  • {topic}" for topic in self.trends_data.get('hot_topics', [])[:5]])}

🛠️ POPULAR FRAMEWORKS/TAGS:
{chr(10).join([f"  • {fw}" for fw in self.trends_data.get('popular_frameworks', [])[:10]])}

💡 INDUSTRY BUZZWORDS:
{', '.join(self.trends_data.get('industry_buzzwords', [])[:20])}
"""
        return summary
    
    def get_context_for_ai(self):
        """Get trends data formatted for AI context"""
        return {
            'trending_tech': [t['name'] for t in self.trends_data.get('trending_technologies', [])[:10]],
            'hot_topics': self.trends_data.get('hot_topics', [])[:10],
            'popular_frameworks': self.trends_data.get('popular_frameworks', [])[:15],
            'buzzwords': self.trends_data.get('industry_buzzwords', [])[:30],
            'last_updated': self.trends_data.get('last_updated', 'Unknown')
        }


def main():
    """Test the scraper"""
    scraper = TechTrendsScraper()
    
    # Update trends
    scraper.update_all_trends()
    
    # Print summary
    print("\n" + scraper.get_trends_summary())
    
    # Print AI context
    print("\n📊 AI CONTEXT DATA:")
    print(json.dumps(scraper.get_context_for_ai(), indent=2))


if __name__ == '__main__':
    main()
