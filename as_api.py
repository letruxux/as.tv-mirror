# https://github.com/Mortafix/Saturno/blob/main/saturno/anime.py

from re import search as _search
from bs4 import BeautifulSoup as _bs
from aiohttp import ClientSession as _CS
from typing import Any as _Any
from urllib.parse import quote as _encode
from json import loads as _dictify
import asyncio as _asyncio
from warnings import warn as _warn

BASE_URL = "https://www.animesaturn.tv"


async def _get(url: str):
    async with _CS() as sess:
        return await (await sess.get(url)).text()


def _extract(input_string: str, marker: str):
    start_index = input_string.find(marker)
    if start_index == -1:
        return ""

    end_index = input_string.find(marker, start_index + 1)
    if end_index == -1:
        return ""

    result = input_string[start_index + 1 : end_index]

    return result


async def get_episodes_link(anime_link: str) -> tuple[list[str], list[int]]:
    soup = _bs(await _get(anime_link), "html.parser")
    if not soup.find("div", {"class": "tab-content"}):
        return None, None
    a_refs = soup.find("div", {"class": "tab-content"}).findAll("a")
    links = [link.get("href") for link in a_refs]
    episodes = [int(_search(r"ep-(\d+)", link.get("href")).group(1)) for link in a_refs]

    # ["/ep1", "/ep2"], [1, 2]
    return links, episodes


async def get_download_link(
    episode_link: str, get_m3u8: bool = False
) -> tuple[str, str]:
    soup = _bs(await _get(episode_link), "html.parser")
    ep_page = soup.find("div", {"class": "card-body"}).find("a").get("href")

    playlist = ""
    if get_m3u8:
        ep_soup = _bs(await _get(ep_page), "html.parser")
        link = _search(r"\"(.*\.(m3u8|mp4))\"", str(ep_soup))
        playlist = link.group(1) or (s := ep_soup.find("source")) and s.get("src")

    return ep_page, playlist


async def get_anime_info(anime_link: str) -> dict[str, _Any]:
    try:
        soup = _bs(await _get(anime_link), "html.parser")

        if not soup.find("div", {"class": "tab-content"}):
            return None, None

        cover_url = next(
            (
                img["src"]
                for img in soup.find_all(
                    attrs={"class": "img-fluid cover-anime rounded"}
                )
            ),
            None,
        )

        banner_url = next(
            (_extract(style, "'") for style in [soup.select_one(".banner")["style"]]),
            None,
        )

        title = next(
            (
                title_elem.select("b")[0].text
                for title_elem in soup.find_all(
                    attrs={"class": "container anime-title-as mb-3 w-100"}
                )
            ),
            None,
        )

        tags = [
            tag.text
            for tag in soup.find_all(
                attrs={"class": "badge badge-light generi-as mb-1"}
            )
        ]

        return {
            "banner_url": banner_url,
            "tags": tags,
            "cover_url": cover_url,
            "title": title,
        }
    except:
        return None


async def api_search(query: str) -> list[tuple[str, str]]:
    url = f"{BASE_URL}/index.php?search=1&key=" + _encode(query)
    data = _dictify(await _get(url))

    return [(r.get("name"), f"{BASE_URL}/anime/{r.get('link')}") for r in (data)]
