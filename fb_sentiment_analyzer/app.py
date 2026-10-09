from flask import Flask, render_template, request, jsonify
from fb_client import FacebookClient
from analyzer import SentimentAnalyzer

app = Flask(__name__)
analyzer = SentimentAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json() or {}
    
    topic = data.get('topic', 'Bitcoin').strip()
    if not topic:
        return jsonify({'error': 'Topic / search word is required'}), 400

    min_likes = data.get('min_likes', 10)
    min_shares = data.get('min_shares', 2)
    filter_replies = data.get('filter_replies', True)
    post_language = data.get('post_language', 'en')
    sentiment_filter = data.get('sentiment_filter', 'all')
    min_polarity = data.get('min_polarity', 0.0)
    fb_token = data.get('fb_access_token', '').strip()

    # 1. Fetch raw Facebook posts
    fb_client = FacebookClient(access_token=fb_token if fb_token else None)
    raw_posts = fb_client.fetch_posts(topic=topic, limit=40)

    # 2. Filter & analyze tone via NLTK VADER
    params = {
        'min_likes': min_likes,
        'min_shares': min_shares,
        'filter_replies': filter_replies,
        'post_language': post_language,
        'sentiment_filter': sentiment_filter,
        'min_polarity': min_polarity
    }
    
    results = analyzer.filter_and_analyze_posts(raw_posts, params)
    results['topic'] = topic
    results['using_live_api'] = bool(fb_token)

    return jsonify(results)

@app.route('/api/sample_topics', methods=['GET'])
def sample_topics():
    return jsonify({
        'topics': ['Bitcoin', 'AI', 'Stocks', 'Metaverse', 'Electric Vehicles', 'Renewable Energy']
    })

if __name__ == '__main__':
    print("[SERVER] Starting Facebook Sentiment Analyzer Bot web app on http://127.0.0.1:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
