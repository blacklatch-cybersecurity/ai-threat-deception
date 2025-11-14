var map = L.map('map').setView([20, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

function loadEvents() {
    fetch("/api/events")
    .then(r => r.json())
    .then(events => {
        const box = document.getElementById("events");
        box.innerHTML = "";

        events.forEach(e => {
            let div = document.createElement("div");
            div.classList.add("event");

            if (e.score > 0.8) div.classList.add("critical");
            else if (e.score > 0.5) div.classList.add("high");
            else if (e.score > 0.3) div.classList.add("medium");
            else div.classList.add("low");

            div.innerHTML = `
                <b>${e.ip}</b> → ${e.cmd}<br>
                intent: ${e.intent} | score: ${e.score.toFixed(2)}
            `;

            box.appendChild(div);

            L.marker([e.lat, e.lon]).addTo(map);
        })
    });
}

setInterval(loadEvents, 1500);
