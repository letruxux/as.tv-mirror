"use strict";

document.documentElement.setAttribute("data-theme", "dark");

const banner = document.querySelector("#banner");
const title = document.querySelector("#title");
const episodesDiv = document.querySelector("#episodes");
const directEpisode = document.querySelector("input");
const overDiv = document.querySelector("#over");

function zip(...arrays) {
    return arrays[0].map((_, i) => arrays.map((array) => array[i]));
}

async function fetchData(url) {
    const response = await fetch(url);
    const text = await response.text();
    return JSON.parse(text);
}

async function getData() {
    const url = "/info?url=" + document.body.getAttribute("url");
    return fetchData(url);
}

async function getEpisodes() {
    const url = "/episodes?url=" + document.body.getAttribute("url");
    return fetchData(url);
}

async function getEpisode(epUrl) {
    const url = "/episode?url=" + epUrl;
    return fetchData(url);
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

    document.title = data.title;
    title.textContent = data.title;

    episodesDiv.style.opacity = "1";
    episodesDiv.innerHTML = "Loading episodes...";

    fadeOut();

    const episodes = await getEpisodes();
    const name = `${data.title} (${episodes.episodes.length})`;

    document.title = name;
    title.textContent = name;

    function update(specify) {
        episodesDiv.innerHTML = "";
        zip(episodes.episodes, episodes.links).forEach(([ep, epUrl]) => {
            if (ep.toString().includes(specify)) {
                const e = document.createElement("a");
                e.setAttribute("href", "/episode?url=" + epUrl);
                e.textContent = ep;
                episodesDiv.appendChild(e);
            }
        });
    }

    update("");

    directEpisode.addEventListener("input", () => {
        update(directEpisode.value);
    });
})();
