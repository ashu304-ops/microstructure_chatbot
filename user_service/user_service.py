from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("/app/users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, username TEXT)")
    c.execute("INSERT OR REPLACE INTO users (user_id, username) VALUES (?, ?)", ("user1", "Test User"))
    conn.commit()
    conn.close()

@app.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    conn = sqlite3.connect("/app/users.db")
    c = conn.cursor()
    c.execute("SELECT user_id, username FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({"user_id": user[0], "username": user[1]})
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001, debug=True)