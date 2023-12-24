# https://github.com/Mortafix/Saturno/blob/main/saturno/anime.py

from re import search as _search
from bs4 import BeautifulSoup as _bs
from aiohttp import ClientSession as _CS
from yt_dlp import YoutubeDL as _DL


async def get(url: str):
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


def download_video(url, filename):
    with _DL(
        {
            "outtmpl": filename,
            "quiet": False,
            "no_warnings": True,
            "nocheckcertificate": True,
        }
    ) as ydl:
        ydl.download([url])


async def search_anime(query):
    soup = _bs(
        await get(f"https://www.animesaturn.tv/animelist?search={query}"), "html.parser"
    )
    return [
        (group.find("h3").text[1:-1], group.find("a").get("href"))
        for group in soup.findAll("ul", {"class": "list-group"})
    ]


async def get_episodes_link(anime_link) -> tuple[list[str], list[int]]:
    soup = _bs(await get(anime_link), "html.parser")
    if not soup.find("div", {"class": "tab-content"}):
        return None, None
    a_refs = soup.find("div", {"class": "tab-content"}).findAll("a")
    links = [link.get("href") for link in a_refs]
    episodes = [int(_search(r"ep-(\d+)", link.get("href")).group(1)) for link in a_refs]
    return links, episodes


async def get_download_link(episode_link):
    soup = _bs(await get(episode_link), "html.parser")
    ep_page = soup.find("div", {"class": "card-body"}).find("a").get("href")
    ep_soup = _bs(await get(ep_page), "html.parser")
    link = _search(r"\"(.*\.(m3u8|mp4))\"", str(ep_soup))
    return ep_page, (link.group(1) or (s := ep_soup.find("source")) and s.get("src"))


async def get_anime_info(anime_link):
    try:
        soup = _bs(await get(anime_link), "html.parser")

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
