from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from youtube_api import YouTubeAPI
from ballet_search import BalletSearchEngine


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Initialise Youtube API
youtube_api = YouTubeAPI()
search_engine = None # Will be initialised after loading ballets

def load_ballets():
    """Load ballet data from JSON file"""
    with open("data/ballets.json", "r") as f:
        return json.load(f)

def init_search_engine():
    """Initialise search engine with ballet data"""
    global search_engine
    ballets = load_ballets()
    search_engine = BalletSearchEngine(ballets)
    return ballets

def load_bookmarks():
    """Load user bookmarks"""
    if os.path.exists("data/bookmarks.json"):
        with open("data/bookmarks.json", "r") as f:
            return json.load(f)
    return []

def save_bookmark(video_data, note):
    """Save a video bookmark with user note"""
    bookmarks = load_bookmarks()
    bookmark = {
        'video_id': video_data['id'],
        'title': video_data['title'],
        'note': note,
        'embed_url': video_data['embed_url']
    }
    bookmarks.append(bookmark)

    with open("data/bookmarks.json", "w") as f:
        json.dump(bookmarks, f, indent=2)

@app.route("/")
def index():
    """Home page with ballet grid"""
    ballets = init_search_engine()
    return render_template("index.html", ballets=ballets)

@app.route("/ballets/<ballet_id>")
def ballet_details(ballet_id):
    """Ballet details page with videos"""
    try:
        ballets = load_ballets()

        if search_engine is None:
            init_search_engine()

        if ballet_id not in ballets:
            return render_template("error.html", error="Ballet not found"), 404
        
        ballet = ballets[ballet_id]
        
        # OPTIMIZATION: Build one comprehensive search query
        search_query = search_engine.build_default_search_query(ballet_id)
        
        # SINGLE API CALL instead of multiple
        videos = youtube_api.search_videos(search_query, max_results=12)
        
        return render_template("ballet_details.html", ballet=ballet, ballet_id=ballet_id, videos=videos)
    except Exception as e:
        app.logger.error(f"Error loading ballet details: {e}")
        return render_template("error.html", error="Something went wrong loading this ballet"), 500

@app.route("/ballet/search-suggestions/<ballet_id>")
def get_search_suggestions(ballet_id):
    """Get search suggestions for a ballet"""
    if search_engine is None:
        init_search_engine()
    
    suggestions = search_engine.suggest_searches(ballet_id)
    return jsonify({"suggestions": suggestions})

@app.route("/ballet/custom-search/<ballet_id>")
def custom_search(ballet_id):
    """Custom search for a ballet"""
    if search_engine is None:
        init_search_engine()
    
    # Check if it's a from suggestion
    direct_query = request.args.get('query')
    if direct_query:
        videos = youtube_api.search_videos(direct_query, max_results=10)
        return jsonify({"query": direct_query, "videos": videos})
    
    # Get custom search parameters
    character = request.args.get('character') # access URL query parameters
    act = request.args.get('act', type=int)
    scene_type = request.args.get('scene_type')
    
    query = search_engine.build_search_query(
        ballet_id,
        character=character,
        act=act,
        scene_type=scene_type
    )

    videos = youtube_api.search_videos(query, max_results=10)
    return jsonify({"query": query, "videos": videos})

@app.route("/add_bookmark", methods=["POST"])
def add_bookmark():
    """Add a video bookmark with user note"""
    video_data = request.json.get('video')
    note = request.json.get('note', '')

    save_bookmark(video_data, note)
    return jsonify({"status": 'success'})

@app.route("/bookmarks")
def bookmarks():
    """View all bookmarks"""
    user_bookmarks = load_bookmarks()
    return render_template("bookmarks.html", bookmarks=user_bookmarks)

@app.route("/remove_bookmark/<int:bookmark_index>", methods=["POST"])
def remove_bookmark(bookmark_index):
    """Remove a bookmark"""
    try:
        user_bookmarks = load_bookmarks()
        if 0 <= bookmark_index < len(user_bookmarks):
            user_bookmarks.pop(bookmark_index)
            with open("data/bookmarks.json", "w") as f:
                json.dump(user_bookmarks, f, indent=2)
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Bookmark not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)