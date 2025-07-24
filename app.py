from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import re
from collections import Counter

app = Flask(__name__)
CORS(app)

# Data storage file
DATA_FILE = 'messages.json'
ALERTS_FILE = 'alerts.json'

# Sentiment analysis keywords
SENTIMENT_KEYWORDS = {
    'angry': ['hate', 'terrible', 'awful', 'worst', 'broken', 'bug', 'error', 'crash', 'fail', 'stupid', 'useless', 'garbage', 'angry', 'frustrated', 'annoyed'],
    'confused': ['confused', 'help', 'how', 'what', 'where', 'why', 'unclear', 'understand', 'lost', 'stuck', 'don\'t know', 'unclear'],
    'delighted': ['love', 'amazing', 'great', 'excellent', 'perfect', 'awesome', 'fantastic', 'wonderful', 'brilliant', 'happy', 'satisfied', 'pleased'],
    'neutral': ['okay', 'fine', 'normal', 'standard', 'regular', 'average']
}

def load_data(filename):
    """Load data from JSON file"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(filename, data):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def analyze_sentiment(text):
    """Analyze sentiment of text using keyword matching"""
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    sentiment_scores = {
        'angry': 0,
        'confused': 0,
        'delighted': 0,
        'neutral': 0
    }
    
    found_keywords = []
    
    # Count keyword matches
    for word in words:
        for sentiment, keywords in SENTIMENT_KEYWORDS.items():
            if word in keywords:
                sentiment_scores[sentiment] += 1
                found_keywords.append(word)
    
    # Determine dominant sentiment
    max_sentiment = max(sentiment_scores, key=sentiment_scores.get)
    max_score = sentiment_scores[max_sentiment]
    
    if max_score == 0:
        sentiment = 'neutral'
        score = 0
    else:
        sentiment = max_sentiment
        if sentiment == 'angry':
            score = -min(max_score * 0.3, 1.0)
        elif sentiment == 'confused':
            score = -min(max_score * 0.2, 0.5)
        elif sentiment == 'delighted':
            score = min(max_score * 0.3, 1.0)
        else:
            score = 0
    
    return {
        'sentiment': sentiment,
        'score': round(score, 2),
        'keywords': list(set(found_keywords))
    }

def check_sentiment_spike():
    """Check for sentiment spikes and create alerts"""
    messages = load_data(DATA_FILE)
    if len(messages) < 5:
        return
    
    # Get last 10 messages
    recent_messages = messages[:10]
    angry_count = sum(1 for msg in recent_messages if msg['sentiment'] == 'angry')
    angry_percentage = angry_count / len(recent_messages)
    
    alerts = load_data(ALERTS_FILE)
    
    # Check if we already have a recent similar alert
    now = datetime.now()
    recent_alerts = [a for a in alerts if 
                    datetime.fromisoformat(a['timestamp']) > now - timedelta(minutes=5)]
    
    if angry_percentage > 0.5 and not any(a['type'] == 'critical' for a in recent_alerts):
        alert = {
            'id': str(int(now.timestamp() * 1000)),
            'type': 'critical',
            'message': f'High negative sentiment detected: {int(angry_percentage * 100)}% of recent messages are angry',
            'timestamp': now.isoformat(),
            'acknowledged': False
        }
        alerts.insert(0, alert)
        save_data(ALERTS_FILE, alerts)
    elif angry_percentage > 0.3 and not any(a['type'] == 'warning' for a in recent_alerts):
        alert = {
            'id': str(int(now.timestamp() * 1000)),
            'type': 'warning',
            'message': f'Elevated negative sentiment: {int(angry_percentage * 100)}% of recent messages are angry',
            'timestamp': now.isoformat(),
            'acknowledged': False
        }
        alerts.insert(0, alert)
        save_data(ALERTS_FILE, alerts)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/message', methods=['POST'])
def analyze_message():
    """Analyze sentiment of incoming message"""
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400
    
    message_text = data['message']
    analysis = analyze_sentiment(message_text)
    
    # Store message
    messages = load_data(DATA_FILE)
    message_data = {
        'id': str(int(datetime.now().timestamp() * 1000)),
        'text': message_text,
        'sentiment': analysis['sentiment'],
        'score': analysis['score'],
        'keywords': analysis['keywords'],
        'timestamp': datetime.now().isoformat()
    }
    
    messages.insert(0, message_data)
    # Keep only last 100 messages
    messages = messages[:100]
    save_data(DATA_FILE, messages)
    
    # Check for sentiment spikes
    check_sentiment_spike()
    
    return jsonify(analysis)

@app.route('/api/messages')
def get_messages():
    """Get all messages with optional filtering"""
    messages = load_data(DATA_FILE)
    
    sentiment_filter = request.args.get('sentiment')
    search_query = request.args.get('search', '').lower()
    
    if sentiment_filter and sentiment_filter != 'all':
        messages = [msg for msg in messages if msg['sentiment'] == sentiment_filter]
    
    if search_query:
        messages = [msg for msg in messages if 
                   search_query in msg['text'].lower() or 
                   any(search_query in keyword for keyword in msg['keywords'])]
    
    return jsonify(messages)

@app.route('/api/trends')
def get_trends():
    """Get sentiment trends for the last 24 hours"""
    messages = load_data(DATA_FILE)
    trends = []
    
    now = datetime.now()
    for i in range(23, -1, -1):
        hour_start = now - timedelta(hours=i)
        hour_key = hour_start.strftime('%H:00')
        
        hour_messages = [msg for msg in messages if 
                        datetime.fromisoformat(msg['timestamp']).hour == hour_start.hour]
        
        counts = {
            'angry': len([m for m in hour_messages if m['sentiment'] == 'angry']),
            'confused': len([m for m in hour_messages if m['sentiment'] == 'confused']),
            'neutral': len([m for m in hour_messages if m['sentiment'] == 'neutral']),
            'delighted': len([m for m in hour_messages if m['sentiment'] == 'delighted'])
        }
        
        trends.append({
            'hour': hour_key,
            **counts
        })
    
    return jsonify(trends)

@app.route('/api/alerts')
def get_alerts():
    """Get all alerts"""
    alerts = load_data(ALERTS_FILE)
    return jsonify(alerts)

@app.route('/api/alerts/<alert_id>/acknowledge', methods=['POST'])
def acknowledge_alert(alert_id):
    """Acknowledge an alert"""
    alerts = load_data(ALERTS_FILE)
    
    for alert in alerts:
        if alert['id'] == alert_id:
            alert['acknowledged'] = True
            break
    
    save_data(ALERTS_FILE, alerts)
    return jsonify({'success': True})

@app.route('/api/stats')
def get_stats():
    """Get overall statistics"""
    messages = load_data(DATA_FILE)
    
    stats = {
        'total': len(messages),
        'angry': len([m for m in messages if m['sentiment'] == 'angry']),
        'confused': len([m for m in messages if m['sentiment'] == 'confused']),
        'neutral': len([m for m in messages if m['sentiment'] == 'neutral']),
        'delighted': len([m for m in messages if m['sentiment'] == 'delighted'])
    }
    
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)