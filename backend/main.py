from flask import Flask, request, jsonify
from avl_tree import AVLDictionary
from flask_cors import CORS
from difflib import get_close_matches

app = Flask(__name__)
CORS(app)  # Cho phép frontend truy cập

dictionary = AVLDictionary()

@app.route("/search", methods=["GET"])
def search():
    word = request.args.get("word", "").strip().lower()
    if not word:
        return jsonify({"error": "Thiếu tham số 'word'"}), 400
    meaning = dictionary.find_meaning(word)
    if meaning:
        return jsonify({"word": word, "meaning": meaning})
    else:
        suggestions = get_close_matches(word, dictionary.get_all_words().keys(), n=5, cutoff=0.6)
        return jsonify({
            "error": "Không tìm thấy từ.",
            "suggestions": suggestions
        }), 404

@app.route("/add", methods=["POST"])
def add_word():
    data = request.json
    word = data.get("word", "").strip().lower()
    meaning = data.get("meaning", "").strip()
    if not word or not meaning:
        return jsonify({"error": "Thiếu 'word' hoặc 'meaning'"}), 400
    dictionary.add_word(word, meaning)
    return jsonify({"message": f"Đã thêm từ '{word}'"})

@app.route("/delete", methods=["DELETE"])
def delete_word():
    word = request.args.get("word", "").strip().lower()
    if not word:
        return jsonify({"error": "Thiếu tham số 'word'"}), 400
    dictionary.delete_word(word)
    return jsonify({"message": f"Đã xoá từ '{word}' nếu tồn tại"})

@app.route("/all", methods=["GET"])
def get_all():
    words = dictionary.get_all_words()
    return jsonify(words)

if __name__ == "__main__":
    app.run(debug=True)
