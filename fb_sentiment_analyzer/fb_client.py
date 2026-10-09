import random
import requests
from datetime import datetime, timedelta

class FacebookClient:
    def __init__(self, access_token: str = None):
        self.access_token = access_token
        self.graph_url = "https://graph.facebook.com/v19.0"

    def fetch_posts(self, topic: str, limit: int = 30) -> list:
        """
        Fetches posts related to topic. Uses real Graph API if access_token is set,
        otherwise falls back to generating realistic mock Facebook posts for the topic.
        """
        if self.access_token:
            try:
                # FB Graph API Search / Feed endpoint call
                url = f"{self.graph_url}/search"
                params = {
                    'q': topic,
                    'type': 'post',
                    'fields': 'id,message,created_time,shares,likes.summary(true),comments.summary(true),parent_id',
                    'limit': limit,
                    'access_token': self.access_token
                }
                resp = requests.get(url, params=params, timeout=10)
                if resp.status_code == 200:
                    data = resp.json().get('data', [])
                    formatted = []
                    for item in data:
                        shares_count = item.get('shares', {}).get('count', 0) if isinstance(item.get('shares'), dict) else 0
                        likes_count = item.get('likes', {}).get('summary', {}).get('total_count', 0)
                        comments_count = item.get('comments', {}).get('summary', {}).get('total_count', 0)
                        is_reply = 'parent_id' in item or item.get('is_reply', False)

                        formatted.append({
                            'id': item.get('id'),
                            'author': 'Facebook User',
                            'author_avatar': f"https://api.dicebear.com/7.x/identicon/svg?seed={item.get('id')}",
                            'created_time': item.get('created_time', datetime.now().isoformat()),
                            'message': item.get('message', ''),
                            'likes': likes_count,
                            'shares': shares_count,
                            'comments_count': comments_count,
                            'is_reply': is_reply,
                            'post_url': f"https://facebook.com/{item.get('id')}"
                        })
                    return formatted
            except Exception as e:
                print(f"[FacebookClient] Graph API error, falling back to simulation: {e}")

        # Fallback / Demo Mode: Generate realistic topic-specific FB posts
        return self._generate_mock_fb_posts(topic, limit)

    def _generate_mock_fb_posts(self, topic: str, limit: int = 30) -> list:
        """
        Generates realistic sample Facebook posts tailored to the provided topic (e.g. Bitcoin, AI, Stocks)
        including realistic counts of likes, shares, comments, and replies for filter testing.
        """
        topic_lower = topic.lower()

        positive_templates = [
            f"Extremely bullish on {topic}! The technology and adoption trends are breaking records this quarter. 🚀📈",
            f"Just finished reviewing the latest report on {topic}. Outstanding results and huge growth potential ahead!",
            f"If you're not paying attention to {topic} right now, you are missing out on the biggest shift of our decade. Absolutely groundbreaking!",
            f"Love how accessible {topic} has become. The ecosystem is evolving so rapidly and benefiting everyone involved. 👍🏼✨",
            f"Great news for everyone following {topic}! Key metrics show massive institutional confidence and user satisfaction.",
            f"{topic} is solving real-world problems. Impressed by the team's commitment to security, speed, and innovation.",
            f"A fantastic update for {topic} enthusiasts! Community engagement is at an all-time high.",
            f"Investing time into learning about {topic} was the best decision I made this year. High returns and super bright future!"
        ]

        negative_templates = [
            f"Really disappointed with the recent updates around {topic}. High volatility and lack of clear regulation remain a huge risk. ⚠️",
            f"Warning to everyone researching {topic}: lots of hype, bad execution, and terrible customer feedback lately.",
            f"Is it just me, or has {topic} completely lost its momentum? Scams and exaggerated promises everywhere.",
            f"Severe crash in confidence regarding {topic}. Prices are falling and early adopters are exiting fast. 📉",
            f"Why is no one talking about the major flaws in {topic}? The costs are skyrocketing while reliability drops.",
            f"Frustrated with {topic} platform downtime and missing features. Major setback for users."
        ]

        neutral_templates = [
            f"Here is a neutral summary of current developments in {topic}: Market volume remains steady with mixed analyst opinions.",
            f"What are your thoughts on {topic}? Some predict steady growth while others advise caution. Let's discuss in the comments.",
            f"Attending the annual global conference on {topic} today. Looking forward to hearing different perspectives.",
            f"Interesting analysis comparing {topic} performance over the last 3 years versus traditional benchmarks.",
            f"Key takeaway from today's discussion on {topic}: execution and timing will determine long-term success.",
            f"Sharing an educational guide explaining the fundamentals of {topic} for beginners."
        ]

        reply_templates = [
            f"Replying to @tech_guru: Totally agree regarding {topic}! Thanks for sharing this breakdown.",
            f"Comment reply: I don't think {topic} will sustain this rate, let's wait for next month's report.",
            f"Replying to post: Can you share the source link for these {topic} statistics?",
            f"Comment: Thanks for explaining {topic}, very helpful comment!"
        ]

        authors = [
            "Sarah Jenkins", "Crypto Insider Daily", "Alex Rivera", "Tech Pulse Magazine",
            "Marcus Chen", "Financial Horizon", "Elena Rostova", "Market Insights",
            "David Miller", "Digital Trends Today", "Rachel Adams", "Global Venture Hub"
        ]

        posts = []
        now = datetime.now()

        for i in range(1, limit + 1):
            is_reply = (i % 5 == 0) # 20% of posts are replies/comments
            
            if is_reply:
                msg = random.choice(reply_templates)
                likes = random.randint(0, 15)
                shares = random.randint(0, 3)
            else:
                rand_val = random.random()
                if rand_val < 0.45:
                    msg = random.choice(positive_templates)
                elif rand_val < 0.75:
                    msg = random.choice(negative_templates)
                else:
                    msg = random.choice(neutral_templates)

                # Generate varied engagement numbers to test user filters (e.g. min likes 10, min shares 2)
                likes = random.choice([2, 5, 12, 28, 45, 110, 250, 430, 890])
                shares = random.choice([0, 1, 3, 7, 14, 32, 85, 120])

            created_time = (now - timedelta(hours=random.randint(1, 72))).strftime('%Y-%m-%dT%H:%M:%SZ')
            author = random.choice(authors)

            posts.append({
                'id': f"fb_post_{i}_{random.randint(1000, 9999)}",
                'author': author,
                'author_avatar': f"https://api.dicebear.com/7.x/avataaars/svg?seed={author.replace(' ', '')}",
                'created_time': created_time,
                'message': msg,
                'likes': likes,
                'shares': shares,
                'comments_count': random.randint(1, 45),
                'is_reply': is_reply,
                'post_url': f"https://facebook.com/posts/{i}"
            })

        return posts
