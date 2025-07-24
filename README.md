# 🐶 Sentimental Watchdog

**An AI-powered emotional trend detector for customer support teams.**

---

## 📌 Overview

Customer support teams often struggle to track emotional shifts in user messages across emails, chats, and help desk platforms. By the time trends like frustration or confusion are noticed, it's usually too late.

**Sentimental Watchdog** is a real-time sentiment monitoring system that uses NLP to analyze incoming support messages, detect emotion, and trigger alerts for quick intervention. It's designed to improve customer satisfaction and reduce churn by helping support teams act before issues escalate.

---

## 💡 Problem Statement

Support teams communicate with customers via:
- Support tickets (email-based)
- Live chats
- Help desk systems (e.g., Zendesk, Freshdesk)

But they often miss trends like:
- Spike in angry or confused messages
- Increasing frustration with a feature
- Sudden drops or rises in satisfaction

These trends are currently found through manual reviews or after customer dissatisfaction builds up.

---

## 🎯 Goals

Build an AI agent that:
- ✅ Monitors customer messages in real-time or batch
- ✅ Detects emotional tone (angry, confused, neutral, delighted)
- ✅ Tags messages with sentiment labels
- ✅ Tracks sentiment over time (hourly, daily, weekly)
- ✅ Triggers alerts for negative spikes or positive surges
- ✅ (Optional) Displays insights on a dashboard

---

## 🧱 Tech Stack

| Component       | Technology            |
|-----------------|------------------------|
| **Frontend**    | HTML, CSS, JavaScript  |
| **Backend**     | Python Flask           |
| **Sentiment Analysis** | NLP using BERT or OpenAI API |
| **Storage**     | JSON files (for logs & trend data) |
| **Alert System**| Flask routes / Console logs / Email (configurable) |

---

## 🧠 Features

- 🔍 **Sentiment Analysis:** NLP-powered classification of messages
- 📈 **Trend Tracking:** Aggregates sentiment and detects spikes
- 🚨 **Alert System:** Notifies when negative emotion surges
- 📊 **Dashboard (Optional):** Visualizes sentiment trends and flagged messages

---

## 📁 Project Structure

sentimental-watchdog/
│
├── static/ # CSS, JS assets
├── templates/ # HTML UI files (Dashboard, Alert View)
├── app.py # Flask app entry point
├── sentiment_model.py # NLP logic for emotion detection
├── trends_analyzer.py # Time-based trend aggregation and spike detection
├── data/ # JSON storage (message logs, metrics)
├── README.md # Project documentation


## ⚙️ How It Works

1. **Data Ingestion**
   - Collect messages (emails, chats, tickets)
   - Input can be live (via webhook/API) or simulated

2. **Sentiment Analysis**
   - Classify messages into:
     - `Angry`
     - `Confused`
     - `Neutral`
     - `Satisfied / Delighted`

3. **Trend Detection**
   - Aggregate sentiment by hour/day
   - Detect spikes or drops using simple stats or ML models

4. **Alert Triggering**
   - Set thresholds for emotion spikes
   - Notify support team via logs/email/Slack (optional)

5. **Visualization (Optional)**
   - Dashboard to show real-time emotional breakdown
   - Highlight trending issues or flagged messages

---

## 🧪 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/sentimental-watchdog.git
   cd sentimental-watchdog
## Install dependencies
pip install -r requirements.txt
Run the Flask app
python app.py
Open in browser
http://127.0.0.1:5000/
## 🔮 Future Enhancements
Live integration with platforms like Zendesk, Intercom

Graph-based spike detection (anomaly detection models)

Switch from JSON to structured DB (e.g., MongoDB or SQLite)

Authenticated dashboards for agents and managers

Slack or email-based real-time alert delivery

👩‍💻 Author
Varshini Kancharla

Developer of Sentimental Watchdog
Focus: NLP, Flask, Frontend, Realtime Monitoring

📄 License
This project is licensed under the MIT License.
Feel free to use, modify, and share.

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

📬 Feedback
For questions, suggestions, or feedback, feel free to reach out or open an issue.
