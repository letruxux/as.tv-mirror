"use strict";

document.documentElement.setAttribute("data-theme", "dark");
const search = document.querySelector("input");
const resultsContainer = document.querySelector("ul");
const baseUrl = "https://www.animesaturn.tv";

async function searchFunc(q) {
    const f = await fetch("/search?q=" + q);
    if (!f.ok) {
        throw new Error(`${f.status} ${f.statusText}`);
    }
    return await f.json();
}

search.addEventListener("change", async () => {
    try {
        resultsContainer.style.opacity = "0";
        resultsContainer.innerHTML = "";
        const t = await searchFunc(search.value);
        if (t.length > 0) {
            t.forEach((e) => {
                const element = document.createElement("div");
                element.className = "result";
                element.setAttribute(
                    "onclick",
                    "location.href = '/anime?url=" + e[1] + "'"
                );
                const img = document.createElement("h5");
                img.textContent = e[0];
                element.appendChild(img);
                resultsContainer.appendChild(element);
            });
            resultsContainer.style.opacity = "1";
        } else {
            resultsContainer.style.opacity = "1";
            resultsContainer.innerHTML = "No results";
        }
    } catch (error) {
        console.log(error);
    }
});
