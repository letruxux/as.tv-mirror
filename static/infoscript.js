"use strict";
document.documentElement.setAttribute("data-theme", "dark");

let data;
const banner = document.querySelector("#banner");
const title = document.querySelector("#title");
const episodesDiv = document.querySelector("#episodes");
const directEpisode = document.querySelector("input");
const overDiv = document.querySelector("#over");

function zip(...arrays) {
    return arrays[0].map(function (_, i) {
        return arrays.map(function (array) {
            return array[i];
        });
    });
}

async function getData() {
    const url = "/info?url=" + document.body.getAttribute("url");
    const resp = await fetch(url);
    const text = await resp.text();
    const data = JSON.parse(text);
    return data;
}

async function getEpisodes() {
    const url = "/episodes?url=" + document.body.getAttribute("url");
    const resp = await fetch(url);
    const text = await resp.text();
    const data = JSON.parse(text);
    return data;
}

async function getEpisode(epUrl) {
    const url = "/episode?url=" + epUrl;
    const resp = await fetch(url);
    const text = await resp.text();
    const data = JSON.parse(text);
    return data;
}

function fadeOut() {
    overDiv.style.opacity = "0";
    setTimeout(() => {
        overDiv.style.display = "none";
    }, 250);
}

(async function () {
    const data = await getData();
    banner.setAttribute("src", data.banner_url);

    const episodes = await getEpisodes();
    const name = `${data.title} (${episodes.episodes.length})`;

    document.title = name;
    title.textContent = name;

    function update(specify) {
        Array.from(episodesDiv.children).forEach((e) => e.remove());
        for (const [ep, epUrl] of zip(episodes.episodes, episodes.links)) {
            console.log(ep.toString(), specify);
            if (ep.toString().includes(specify)) {
                const e = document.createElement("a");
                e.setAttribute("href", "/episode?url=" + epUrl);
                e.textContent = ep.toString();
                episodesDiv.appendChild(e);
            }
        }
    }

    update("");

    directEpisode.addEventListener("input", () => {
        update(directEpisode.value);
    });

    fadeOut();
})();
