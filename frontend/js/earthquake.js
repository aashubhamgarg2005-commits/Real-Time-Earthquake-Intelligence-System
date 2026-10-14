/* =====================================================
   EARTHQUAKE DETAILS PAGE JAVASCRIPT
   ===================================================== */


/* ================= EARTHQUAKE DATA ================= */

const earthquakeData = {

    id: "EMSC-20261012-001",

    region: "Panama",

    magnitude: 6.8,

    magnitudeType: "Mw",

    depth: 10,

    latitude: 7.904,

    longitude: -77.230,

    time: "12:38:42",

    date: "12 Oct 2026",

    riskScore: 68,

    riskLevel: "Moderate Risk"

};


/* ================= ELEMENTS ================= */

const regionElement =
    document.getElementById(
        "earthquakeRegion"
    );

const eventIdElement =
    document.getElementById(
        "eventId"
    );

const magnitudeElement =
    document.getElementById(
        "magnitude"
    );

const depthElement =
    document.getElementById(
        "depth"
    );

const coordinatesElement =
    document.getElementById(
        "coordinates"
    );

const eventTimeElement =
    document.getElementById(
        "eventTime"
    );

const riskLevelElement =
    document.getElementById(
        "riskLevel"
    );

const scoreElement =
    document.querySelector(
        "#scoreCircle strong"
    );

const magnitudeProgress =
    document.getElementById(
        "magnitudeProgress"
    );


/* ================= LOAD DATA ================= */

function loadEarthquakeData() {

    if (regionElement) {

        regionElement.textContent =
            earthquakeData.region;

    }


    if (eventIdElement) {

        eventIdElement.textContent =
            "Event ID: " +
            earthquakeData.id;

    }


    if (magnitudeElement) {

        magnitudeElement.textContent =
            earthquakeData.magnitude;

    }


    if (depthElement) {

        depthElement.textContent =
            earthquakeData.depth +
            " km";

    }


    if (coordinatesElement) {

        const latitude =
            formatLatitude(
                earthquakeData.latitude
            );

        coordinatesElement.textContent =
            latitude;

        const small =
            coordinatesElement
                .parentElement
                .querySelector("small");

        if (small) {

            small.textContent =
                formatLongitude(
                    earthquakeData.longitude
                );

        }

    }


    if (eventTimeElement) {

        eventTimeElement.textContent =
            earthquakeData.time;

    }


    if (riskLevelElement) {

        riskLevelElement.textContent =
            earthquakeData.riskLevel;

    }


    if (scoreElement) {

        scoreElement.textContent =
            earthquakeData.riskScore;

    }


    updateMagnitudeBar();

}


/* ================= LATITUDE ================= */

function formatLatitude(latitude) {

    const direction =
        latitude >= 0
            ? "N"
            : "S";

    return (
        Math.abs(latitude).toFixed(3) +
        "° " +
        direction
    );

}


/* ================= LONGITUDE ================= */

function formatLongitude(longitude) {

    const direction =
        longitude >= 0
            ? "E"
            : "W";

    return (
        Math.abs(longitude).toFixed(3) +
        "° " +
        direction
    );

}


/* ================= MAGNITUDE BAR ================= */

function updateMagnitudeBar() {

    if (!magnitudeProgress) {
        return;
    }


    /*
        Maximum magnitude
        assumed = 10

        Example:

        6.8 / 10 = 68%
    */

    const percentage =
        Math.min(
            earthquakeData.magnitude * 10,
            100
        );


    magnitudeProgress.style.width =
        percentage + "%";

}


/* ================= DEPTH CLASSIFICATION ================= */

function getDepthType(depth) {

    if (depth < 70) {

        return "Shallow";

    }

    if (depth < 300) {

        return "Intermediate";

    }

    return "Deep";

}


/* ================= CONSOLE INFO ================= */

console.log(
    "Earthquake Details Loaded:",
    earthquakeData
);

console.log(
    "Depth Classification:",
    getDepthType(
        earthquakeData.depth
    )
);


/* ================= INITIALIZE ================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadEarthquakeData();

    }
);