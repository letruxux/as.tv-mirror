"use strict";
document.documentElement.setAttribute("data-theme", "dark");
const search = document.querySelector("input");
const resultsDiv = document.querySelector("ul");

search.addEventListener("change", async () => {
    try {
        const f = await fetch("/search?q=" + search.value);
        if (!f.ok) {
            throw new Error(`${f.status} ${f.statusText}`);
        }
        const t = await f.json();
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
