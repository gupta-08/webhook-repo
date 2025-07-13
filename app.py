import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

# secrets 
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client    = MongoClient(MONGO_URI)

db         = client["github_events"]
collection = db["events"]

app = Flask(__name__)

# home
@app.route("/")
def home():
    return render_template("index.html")

# webhook receiver 
@app.route("/webhook", methods=["POST"])
def webhook():
    data     = request.json
    gh_event = request.headers.get("X-GitHub-Event")
    utc_now  = datetime.utcnow().isoformat() + "Z"

    if gh_event == "push":
        author     = data["pusher"]["name"]
        to_branch  = data["ref"].split("/")[-1]
        request_id = data["after"]             # commit SHA

        collection.insert_one({
            "request_id":  request_id,
            "author":      author,
            "action":      "PUSH",
            "from_branch": "",
            "to_branch":   to_branch,
            "timestamp":   utc_now
        })

    elif gh_event == "pull_request":
        pr          = data["pull_request"]
        author      = pr["user"]["login"]
        from_br     = pr["head"]["ref"]
        to_br       = pr["base"]["ref"]
        request_id  = pr["id"]
        action_op   = data["action"]
        merged      = pr.get("merged", False)

        if action_op == "opened":
            collection.insert_one({
                "request_id":  request_id,
                "author":      author,
                "action":      "PULL_REQUEST",
                "from_branch": from_br,
                "to_branch":   to_br,
                "timestamp":   pr["created_at"]            # UTC ISO
            })

        elif action_op == "closed" and merged:
            collection.insert_one({
                "request_id":  pr["merge_commit_sha"],
                "author":      author,
                "action":      "MERGE",
                "from_branch": from_br,
                "to_branch":   to_br,
                "timestamp":   pr["merged_at"]             # UTC ISO
            })

    return "OK", 200

#  API for frontend 
@app.route("/events", methods=["GET"])
def get_events():
    date_from  = request.args.get("from")
    act_filter = request.args.get("action") 
    query      = {}

    if act_filter:
        query["action"] = act_filter

    if date_from:
        try:
            dt_from = datetime.fromisoformat(date_from)
            query["timestamp"] = {"$gte": dt_from.isoformat()}
        except ValueError:
            pass

    events = list(collection.find(query).sort("timestamp", -1).limit(100))
    for ev in events:
        ev["_id"] = str(ev["_id"])
    return jsonify(events)


#  entrypoint 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
