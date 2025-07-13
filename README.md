# 📡 GitHub Webhook Event Tracker

A lightweight Flask app that listens to GitHub Webhooks for `push`, `pull_request`, and `merge` events and stores them in MongoDB.  
The frontend displays the latest activity in real-time with filtering by date, time zone, and action type.
###Frontend UI
<img width="1773" height="947" alt="image" src="https://github.com/user-attachments/assets/4c474fd9-771f-4338-a545-c029ba89cb7a" />

## ✨ Features

- Receives GitHub Webhooks for:
  - ✅ Push
  - ✅ Pull Request (Opened)
  - ✅ Merge (Closed + Merged)
- Stores event data in MongoDB
- Displays recent activity with:
  - Live updates (every 15 seconds)
  - Time zone toggle (IST / UTC)
  - Date-based filtering
  - Action-based filtering (Push, PR, Merge)
## 🛠 Tech Stack
- Python 3.x
- Flask
- HTML, CSS, JavaScript
- MongoDB Atlas
- GitHub Webhooks
- LocalTunnel (for exposing localhost)
- 

## 📁 Folder Structure
```
webhook-repo/
├── templates/
│ └── index.html
├── .env # Mongo URI (not committed)
├── app.py # Flask backend
├── requirements.txt # Python dependencies
├── README.md
```
## 🚀 Getting Started

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/webhook-repo.git
cd webhook-repo

```
2. **Create a virtual environment**
```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Set your MongoDB URI**
   Create a .env file:
```bash
MONGO_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/github_events
```
5. **Run the app**
```bash
python app.py
```
6. **Expose your localhost (for GitHub Webhooks)**
```bash
lt --port 5000
```
7. ** Webhook Setup**
## 🪝 Setting Up GitHub Webhook

1. Go to your `action-repo` on GitHub
2. Settings → Webhooks → Add Webhook
3. Payload URL: `https://your-tunnel-url/webhook`
4. Content type: `application/json`
5. Events to send:
   - Just the push event
   - Pull requests
8. ** Environment Variables**
   ## 🔐 Environment Variables

Create a `.env` file in root with:
MONGO_URI=your-mongodb-uri
Make sure `.env` is listed in `.gitignore` to keep it secret.


