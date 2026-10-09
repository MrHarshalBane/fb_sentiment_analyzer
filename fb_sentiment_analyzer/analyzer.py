import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Ensure NLTK VADER lexicon is available
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

class SentimentAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def is_english(self, text: str) -> bool:
        """
        Simple heuristic/regex based check for English text dominance.
        Can be expanded or used with langdetect if needed.
        """
        if not text or len(text.strip()) == 0:
            return False
        # Count ASCII characters vs total alphabet characters
        ascii_chars = sum(1 for c in text if ord(c) < 128)
        return (ascii_chars / len(text)) > 0.85

    def analyze_text(self, text: str) -> dict:
        """
        Analyzes text tone using NLTK VADER.
        Returns compound, pos, neg, neu scores and overall classification.
        """
        scores = self.sia.polarity_scores(text)
        compound = scores['compound']

        if compound >= 0.05:
            tone = 'Positive'
            color = 'green'
        elif compound <= -0.05:
            tone = 'Negative'
            color = 'red'
        else:
            tone = 'Neutral'
            color = 'amber'

        return {
            'compound': round(compound, 4),
            'positive': round(scores['pos'], 4),
            'negative': round(scores['neg'], 4),
            'neutral': round(scores['neu'], 4),
            'tone': tone,
            'color': color
        }

    def filter_and_analyze_posts(self, raw_posts: list, params: dict) -> dict:
        """
        Filters raw posts based on user parameters and calculates overall analytics.

        Params:
        - min_likes (int): default 10
        - min_shares (int): default 2
        - filter_replies (bool): True to exclude comments/replies, False to include
        - post_language (str): 'en' or 'all'
        - sentiment_filter (str): 'all', 'positive', 'negative', 'neutral'
        - min_polarity (float): minimum compound threshold
        """
        min_likes = int(params.get('min_likes', 10))
        min_shares = int(params.get('min_shares', 2))
        filter_replies = params.get('filter_replies', True)
        if isinstance(filter_replies, str):
            filter_replies = filter_replies.lower() in ('true', '1', 'yes')

        post_language = params.get('post_language', 'en')
        sentiment_filter = params.get('sentiment_filter', 'all').lower()
        min_polarity = float(params.get('min_polarity', 0.0))

        processed_posts = []
        total_fetched = len(raw_posts)
        filtered_out_count = 0

        pos_count = 0
        neg_count = 0
        neu_count = 0

        total_likes = 0
        total_shares = 0

        for post in raw_posts:
            # 1. Filter replies / comments
            if filter_replies and post.get('is_reply', False):
                filtered_out_count += 1
                continue

            # 2. Filter min likes
            likes = post.get('likes', 0)
            if likes < min_likes:
                filtered_out_count += 1
                continue

            # 3. Filter min shares / reposts
            shares = post.get('shares', 0)
            if shares < min_shares:
                filtered_out_count += 1
                continue

            # 4. Filter language
            content = post.get('message', '') or post.get('story', '')
            if post_language == 'en' and not self.is_english(content):
                filtered_out_count += 1
                continue

            # 5. Perform Sentiment Analysis
            sentiment = self.analyze_text(content)

            # 6. Sentiment filter & polarity strength check
            if sentiment_filter != 'all':
                if sentiment['tone'].lower() != sentiment_filter:
                    filtered_out_count += 1
                    continue

            if abs(sentiment['compound']) < min_polarity:
                filtered_out_count += 1
                continue

            # Increment stats
            if sentiment['tone'] == 'Positive':
                pos_count += 1
            elif sentiment['tone'] == 'Negative':
                neg_count += 1
            else:
                neu_count += 1

            total_likes += likes
            total_shares += shares

            enriched_post = {
                'id': post.get('id'),
                'author': post.get('author', 'Anonymous FB User'),
                'author_avatar': post.get('author_avatar', ''),
                'created_time': post.get('created_time', ''),
                'message': content,
                'likes': likes,
                'shares': shares,
                'comments_count': post.get('comments_count', 0),
                'is_reply': post.get('is_reply', False),
                'post_url': post.get('post_url', '#'),
                'sentiment': sentiment
            }
            processed_posts.append(enriched_post)

        valid_count = len(processed_posts)
        avg_compound = (
            round(sum(p['sentiment']['compound'] for p in processed_posts) / valid_count, 4)
            if valid_count > 0 else 0
        )

        overall_tone = 'Neutral'
        if avg_compound >= 0.05:
            overall_tone = 'Positive'
        elif avg_compound <= -0.05:
            overall_tone = 'Negative'

        return {
            'summary': {
                'total_fetched': total_fetched,
                'matching_posts': valid_count,
                'filtered_out': filtered_out_count,
                'positive_count': pos_count,
                'negative_count': neg_count,
                'neutral_count': neu_count,
                'positive_percentage': round((pos_count / valid_count * 100), 1) if valid_count else 0,
                'negative_percentage': round((neg_count / valid_count * 100), 1) if valid_count else 0,
                'neutral_percentage': round((neu_count / valid_count * 100), 1) if valid_count else 0,
                'avg_compound_score': avg_compound,
                'overall_tone': overall_tone,
                'total_likes': total_likes,
                'total_shares': total_shares
            },
            'posts': processed_posts
        }
