from quart import Quart, request, render_template, redirect, send_file
from json import dumps as jsonify
import api
import logging

from loggings.log import printf
from loggings import colors

logging.getLogger("hypercorn.access").disabled = True

app = Quart(__name__)


@app.before_request
async def check():
    printf(f"{colors.bold(request.remote_addr)} - {request.method} {request.path}")


@app.route("/")
async def search():
    return await render_template("search.html")


@app.route("/anime")
async def main():
    url = request.args.get("url")
    if not url:
        return "No AnimeSaturn URL provided", 400
    return await render_template("info.html", url=url)


@app.route("/info")
async def api_info():
    url = request.args.get("url")
    if not url:
        return "No AnimeSaturn URL provided", 400

    info = await api.get_anime_info(url)

    if not info:
        return "Invalid AnimeSaturn URL", 400

    return jsonify(info), 200


@app.route("/episodes")
async def api_episodes():
    url = request.args.get("url")
    if not url:
        return "No AnimeSaturn URL provided", 400

    links, episodes = await api.get_episodes_link(url)

    if not (links and episodes):
        return "Invalid AnimeSaturn URL or no episodes", 400

    return jsonify({"links": links, "episodes": episodes}), 200


@app.route("/search")
async def api_search():
    query = request.args.get("q")
    if not query:
        return "No query provided", 400

    results: list[tuple[str, str]] = await api.search_anime(query)

    if not (results):
        return [], 200

    return jsonify(results), 200


@app.route("/episode")
async def api_episode():
    url = request.args.get("url")
    if not url:
        return "No AnimeSaturn URL provided", 400

    player, playlist = await api.get_download_link(url)

    if not player:
        return "Invalid AnimeSaturn URL or no episodes", 400

    return redirect(player)


@app.route("/favicon.ico")
async def favicon():
    return await send_file("static/favicon.ico")


app.run(debug=False)
