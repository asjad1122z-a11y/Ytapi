from flask import Flask, request
import requests

app = Flask(__name__)

API_KEY = "YOUR_YOUTUBE_API_KEY"  # <-- Replace this with your key

def format_channel_info(data, handle):
    snippet = data["snippet"]
    stats = data["statistics"]
    
    return f"""
[C][FF0000]╭[FF0000]─[FF0000]╮[FFFFFF]
[C][B][FF0000]│[FFFFFF]▶[FF0000] │[FFFFFF]║[00BFFF]YOUTUBE INFO[FFFFFF]║
[C][B][FF0000]╰[FF0000]─[FF0000]╯[FFFFFF]
[C][B][FF00FF]━━━━━━━━━━━
[C][B][FFFFFF]Channel Name : [FFFF00]{snippet.get('title', 'Unknown')}
[C][B][FFFFFF]Channel ID    : [FFFF00]{data.get('id', 'Unknown')}
[C][B][FFFFFF]Handle        : [00BFFF]@{handle}
[C][B][FFFFFF]Subscribers   : [00BFFF]{stats.get('subscriberCount', '0')}
[C][B][FFFFFF]Views         : [00BFFF]{stats.get('viewCount', '0')}
[C][B][FFFFFF]Videos        : [00BFFF]{stats.get('videoCount', '0')}
[C][B][FFFFFF]Published At  : [00BFFF]{snippet.get('publishedAt', 'Unknown')}
[C][B][00FFFF]━━━━━━━━━━━
[C][B][FFFFFF]Developer     : Ayaan
"""

@app.route("/yt-info/yt")
def yt_info():
    channel = request.args.get("channel")
    if not channel:
        return "Error: channel parameter is required", 400

    # Call YouTube API by handle
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&forUsername={channel}&key={API_KEY}"
    r = requests.get(url).json()

    # fallback: if channel not found by handle, try by ID
    if not r.get("items"):
        url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel}&key={API_KEY}"
        r = requests.get(url).json()

    if not r.get("items"):
        return f"Channel '{channel}' not found", 404

    data = r["items"][0]
    return format_channel_info(data, channel)
