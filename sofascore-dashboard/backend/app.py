from flask import Flask, jsonify
from scrape import scrape_manchester_united_stats

app = Flask(__name__)

@app.route("/api/team/manchester-united", methods=["GET"])
def get_manchester_united_stats():
    stats = scrape_manchester_united_stats()
    if "error" in stats:
        return jsonify({"error": stats["error"]}), 404
    return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True)
