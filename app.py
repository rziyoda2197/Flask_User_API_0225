from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER
    )
    """)
    conn.commit()
    conn.close()

init_db()


@app.route("/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    return jsonify(users)


@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    name = data.get("name")
    age = data.get("age")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

    return jsonify({"message": "User added"}), 201


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})


if __name__ == "__main__":
    app.run(debug=True)
