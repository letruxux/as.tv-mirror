"use strict";
document.documentElement.setAttribute("data-theme", "dark");
const search = document.querySelector("input");
const resultsDiv = document.querySelector("ul");
const baseUrl = "https://www.animesaturn.tv";

async function searchFuncOld(q) {
    const f = await fetch(baseUrl + "/index.php?search=1&key=" + q, {
        mode: "cors",
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });
    if (!f.ok) {
        throw new Error(`${f.status} ${f.statusText}`);
    }
    const t = await f.json();
    let list = [];
    t.forEach((result) => {
        list.push([result.name, `${baseUrl}/anime/${result.link}`]);
    });
    return list;
}

async function searchFunc(q) {
    const f = await fetch("/search?q=" + q);
    if (!f.ok) {
        throw new Error(`${f.status} ${f.statusText}`);
    }
    return await f.json();
}

search.addEventListener("change", async () => {
    try {
        const t = await searchFunc(search.value);
        resultsDiv.style.opacity = 1;
        Array.from(resultsDiv.children).forEach((e) => e.remove());
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
            resultsDiv.appendChild(element);
        });
    } catch (error) {
        console.log(error);
    }
});
