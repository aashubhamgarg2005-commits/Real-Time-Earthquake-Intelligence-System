/* =========================================
   SEARCH PAGE
========================================= */


/* =========================================
   MOCK EARTHQUAKE DATA
   Later this will come from FastAPI/PostgreSQL
========================================= */

const earthquakeData = [

    {
        id: "EMSC-20261012-001",
        region: "Panama",
        magnitude: 6.8,
        magnitudeType: "Mw",
        depth: 10,
        latitude: 7.904,
        longitude: -77.230,
        date: "2026-10-12",
        time: "12:38:42",
        risk: "High"
    },

    {
        id: "EMSC-20261012-002",
        region: "Japan",
        magnitude: 5.7,
        magnitudeType: "Mw",
        depth: 42,
        latitude: 35.676,
        longitude: 139.650,
        date: "2026-10-12",
        time: "10:21:15",
        risk: "Moderate"
    },

    {
        id: "EMSC-20261012-003",
        region: "Himachal Pradesh, India",
        magnitude: 4.6,
        magnitudeType: "ML",
        depth: 18,
        latitude: 31.104,
        longitude: 77.173,
        date: "2026-10-12",
        time: "08:45:22",
        risk: "Moderate"
    },

    {
        id: "EMSC-20261011-004",
        region: "Indonesia",
        magnitude: 6.1,
        magnitudeType: "Mw",
        depth: 74,
        latitude: -6.200,
        longitude: 106.816,
        date: "2026-10-11",
        time: "21:16:08",
        risk: "High"
    },

    {
        id: "EMSC-20261011-005",
        region: "Turkey",
        magnitude: 3.8,
        magnitudeType: "ML",
        depth: 8,
        latitude: 39.933,
        longitude: 32.859,
        date: "2026-10-11",
        time: "18:32:11",
        risk: "Low"
    },

    {
        id: "EMSC-20261011-006",
        region: "Nepal",
        magnitude: 4.9,
        magnitudeType: "Mw",
        depth: 12,
        latitude: 27.717,
        longitude: 85.324,
        date: "2026-10-11",
        time: "14:17:34",
        risk: "Moderate"
    },

    {
        id: "EMSC-20261010-007",
        region: "California, USA",
        magnitude: 5.2,
        magnitudeType: "Mw",
        depth: 65,
        latitude: 36.778,
        longitude: -119.417,
        date: "2026-10-10",
        time: "11:09:27",
        risk: "Moderate"
    },

    {
        id: "EMSC-20261010-008",
        region: "Uttarakhand, India",
        magnitude: 3.6,
        magnitudeType: "ML",
        depth: 7,
        latitude: 30.066,
        longitude: 79.019,
        date: "2026-10-10",
        time: "06:41:19",
        risk: "Low"
    }

];


/* =========================================
   DOM ELEMENTS
========================================= */

const locationInput = document.getElementById("location");

const minMagnitude = document.getElementById("minMagnitude");
const maxMagnitude = document.getElementById("maxMagnitude");

const minDepth = document.getElementById("minDepth");
const maxDepth = document.getElementById("maxDepth");

const fromDate = document.getElementById("fromDate");
const toDate = document.getElementById("toDate");

const searchBtn = document.getElementById("searchBtn");
const resetBtn = document.getElementById("resetBtn");

const sortSelect = document.getElementById("sortSelect");

const resultsContainer =
    document.getElementById("resultsContainer");

const noResults =
    document.getElementById("noResults");

const resultCount =
    document.getElementById("resultCount");


/* =========================================
   INITIAL LOAD
========================================= */

document.addEventListener("DOMContentLoaded", () => {

    renderResults(earthquakeData);

});


/* =========================================
   SEARCH
========================================= */

searchBtn.addEventListener("click", () => {

    applySearch();

});


/* =========================================
   ENTER KEY SEARCH
========================================= */

document.querySelectorAll(".form-group input").forEach(input => {

    input.addEventListener("keydown", (event) => {

        if (event.key === "Enter") {
            applySearch();
        }

    });

});


/* =========================================
   APPLY SEARCH FILTERS
========================================= */

function applySearch() {

    const location =
        locationInput.value.trim().toLowerCase();

    const minMag =
        parseFloat(minMagnitude.value);

    const maxMag =
        parseFloat(maxMagnitude.value);

    const minDep =
        parseFloat(minDepth.value);

    const maxDep =
        parseFloat(maxDepth.value);

    const startDate =
        fromDate.value;

    const endDate =
        toDate.value;


    let filteredData = earthquakeData.filter(event => {


        /* Location */

        if (location) {

            if (!event.region.toLowerCase().includes(location)) {
                return false;
            }

        }


        /* Minimum magnitude */

        if (!isNaN(minMag)) {

            if (event.magnitude < minMag) {
                return false;
            }

        }


        /* Maximum magnitude */

        if (!isNaN(maxMag)) {

            if (event.magnitude >= maxMag) {
                return false;
            }

        }


        /* Minimum depth */

        if (!isNaN(minDep)) {

            if (event.depth < minDep) {
                return false;
            }

        }


        /* Maximum depth */

        if (!isNaN(maxDep)) {

            if (event.depth > maxDep) {
                return false;
            }

        }


        /* From date */

        if (startDate) {

            if (event.date < startDate) {
                return false;
            }

        }


        /* To date */

        if (endDate) {

            if (event.date > endDate) {
                return false;
            }

        }


        return true;

    });


    sortResults(filteredData);

}


/* =========================================
   SORT RESULTS
========================================= */

sortSelect.addEventListener("change", () => {

    applySearch();

});


function sortResults(data) {

    const sortType = sortSelect.value;


    if (sortType === "latest") {

        data.sort((a, b) => {

            const dateA =
                new Date(`${a.date}T${a.time}`);

            const dateB =
                new Date(`${b.date}T${b.time}`);

            return dateB - dateA;

        });

    }


    if (sortType === "magnitude") {

        data.sort((a, b) => {
            return b.magnitude - a.magnitude;
        });

    }


    if (sortType === "depth") {

        data.sort((a, b) => {
            return b.depth - a.depth;
        });

    }


    renderResults(data);

}


/* =========================================
   RENDER RESULTS
========================================= */

function renderResults(data) {

    resultsContainer.innerHTML = "";

    resultCount.textContent = data.length;


    if (data.length === 0) {

        noResults.classList.remove("hidden");

        return;

    }


    noResults.classList.add("hidden");


    data.forEach(event => {

        const card =
            document.createElement("div");

        card.className = "result-card";


        const magnitudeClass =
            getMagnitudeClass(event.magnitude);

        const riskClass =
            getRiskClass(event.risk);


        card.innerHTML = `

            <div class="magnitude-box ${magnitudeClass}">

                <strong>${event.magnitude.toFixed(1)}</strong>

                <span>${event.magnitudeType}</span>

            </div>


            <div class="event-main">

                <h3>
                    ${event.region}
                </h3>

                <div class="event-meta">

                    <span>
                        <i class="fa-solid fa-clock"></i>
                        ${formatDate(event.date)}
                        ${event.time}
                    </span>

                    <span>
                        <i class="fa-solid fa-arrow-down"></i>
                        ${event.depth} km depth
                    </span>

                    <span>
                        <i class="fa-solid fa-location-dot"></i>
                        ${formatCoordinate(event.latitude, "lat")},
                        ${formatCoordinate(event.longitude, "lon")}
                    </span>

                </div>

            </div>


            <div class="event-actions">

                <div class="event-time">
                    Event ID: ${event.id}
                </div>

                <span class="risk-tag ${riskClass}">
                    ${event.risk} Risk
                </span>

                <br>

                <a
                    href="earthquake.html?id=${event.id}"
                    class="view-btn"
                >
                    View Details
                    <i class="fa-solid fa-arrow-right"></i>
                </a>

            </div>

        `;


        resultsContainer.appendChild(card);

    });

}


/* =========================================
   MAGNITUDE CLASS
========================================= */

function getMagnitudeClass(magnitude) {

    if (magnitude >= 6) {
        return "mag-extreme";
    }

    if (magnitude >= 5) {
        return "mag-high";
    }

    if (magnitude >= 4) {
        return "mag-medium";
    }

    return "mag-low";

}


/* =========================================
   RISK CLASS
========================================= */

function getRiskClass(risk) {

    if (risk === "High") {
        return "risk-high";
    }

    if (risk === "Moderate") {
        return "risk-moderate";
    }

    return "risk-low";

}


/* =========================================
   DATE FORMAT
========================================= */

function formatDate(dateString) {

    const date =
        new Date(`${dateString}T00:00:00`);

    return date.toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "short",
        year: "numeric"
    });

}


/* =========================================
   COORDINATE FORMAT
========================================= */

function formatCoordinate(value, type) {

    const direction =
        type === "lat"
            ? value >= 0 ? "N" : "S"
            : value >= 0 ? "E" : "W";

    return `${Math.abs(value).toFixed(3)}° ${direction}`;

}


/* =========================================
   RESET
========================================= */

resetBtn.addEventListener("click", () => {

    locationInput.value = "";

    minMagnitude.value = "";
    maxMagnitude.value = "";

    minDepth.value = "";
    maxDepth.value = "";

    fromDate.value = "";
    toDate.value = "";

    sortSelect.value = "latest";


    document
        .querySelectorAll(".quick-filter")
        .forEach(button => {
            button.classList.remove("active");
        });


    renderResults(earthquakeData);

});


/* =========================================
   QUICK FILTERS
========================================= */

document
    .querySelectorAll(".quick-filter")
    .forEach(button => {

        button.addEventListener("click", () => {

            document
                .querySelectorAll(".quick-filter")
                .forEach(item => {
                    item.classList.remove("active");
                });

            button.classList.add("active");


            const filter =
                button.dataset.filter;


            /* Reset current filters */

            locationInput.value = "";

            minMagnitude.value = "";
            maxMagnitude.value = "";

            minDepth.value = "";
            maxDepth.value = "";

            fromDate.value = "";
            toDate.value = "";


            let filteredData = [];


            /* Magnitude 6+ */

            if (filter === "m6") {

                filteredData =
                    earthquakeData.filter(
                        event => event.magnitude >= 6
                    );

            }


            /* Last 24 hours */

            else if (filter === "recent") {

                const latestDate =
                    new Date("2026-10-12T23:59:59");

                const previousDate =
                    new Date(latestDate);

                previousDate.setHours(
                    previousDate.getHours() - 24
                );


                filteredData =
                    earthquakeData.filter(event => {

                        const eventDate =
                            new Date(
                                `${event.date}T${event.time}`
                            );

                        return (
                            eventDate >= previousDate &&
                            eventDate <= latestDate
                        );

                    });

            }


            /* Shallow */

            else if (filter === "shallow") {

                filteredData =
                    earthquakeData.filter(
                        event => event.depth <= 20
                    );

            }


            /* India */

            else if (filter === "india") {

                filteredData =
                    earthquakeData.filter(
                        event =>
                            event.region
                                .toLowerCase()
                                .includes("india") ||
                            event.region
                                .toLowerCase()
                                .includes("himachal") ||
                            event.region
                                .toLowerCase()
                                .includes("uttarakhand")
                    );

            }


            sortResults(filteredData);

        });

    });