/* =========================================
   ALERTS PAGE
========================================= */


/* =========================================
   MOCK ALERT DATA
   Later this will come from FastAPI/WebSocket
========================================= */

const alertsData = [

    {
        id: 1,
        type: "high",
        title: "High Magnitude Earthquake Detected",
        message:
            "A magnitude 6.8 Mw earthquake has been detected in Panama. Immediate seismic monitoring is recommended.",
        time: "12:38:42",
        date: "12 Oct 2026",
        eventId: "EMSC-20261012-001",
        unread: true
    },

    {
        id: 2,
        type: "moderate",
        title: "Elevated Seismic Risk",
        message:
            "AI analysis has identified moderate seismic risk for the latest earthquake event.",
        time: "12:39:05",
        date: "12 Oct 2026",
        eventId: "EMSC-20261012-001",
        unread: true
    },

    {
        id: 3,
        type: "info",
        title: "New Earthquake Event",
        message:
            "A magnitude 5.7 Mw earthquake was detected in Japan at a depth of 42 km.",
        time: "10:21:15",
        date: "12 Oct 2026",
        eventId: "EMSC-20261012-002",
        unread: true
    },

    {
        id: 4,
        type: "moderate",
        title: "Aftershock Monitoring Active",
        message:
            "The system has started monitoring potential aftershock activity following a significant earthquake.",
        time: "09:42:18",
        date: "12 Oct 2026",
        eventId: "EMSC-20261012-001",
        unread: false
    },

    {
        id: 5,
        type: "info",
        title: "Seismic Activity Update",
        message:
            "A magnitude 4.6 earthquake has been recorded in Himachal Pradesh, India.",
        time: "08:45:22",
        date: "12 Oct 2026",
        eventId: "EMSC-20261012-003",
        unread: false
    },

    {
        id: 6,
        type: "high",
        title: "High Risk Threshold Triggered",
        message:
            "An earthquake has crossed the configured high-risk threshold. AI-based risk analysis is available.",
        time: "21:16:08",
        date: "11 Oct 2026",
        eventId: "EMSC-20261011-004",
        unread: false
    }

];


/* =========================================
   DOM ELEMENTS
========================================= */

const alertList =
    document.getElementById("alertList");

const emptyAlerts =
    document.getElementById("emptyAlerts");

const activeAlertCount =
    document.getElementById("activeAlertCount");

const highRiskCount =
    document.getElementById("highRiskCount");

const recentEventCount =
    document.getElementById("recentEventCount");

const markAllRead =
    document.getElementById("markAllRead");


/* =========================================
   CURRENT FILTER
========================================= */

let currentFilter = "all";


/* =========================================
   INITIAL LOAD
========================================= */

document.addEventListener("DOMContentLoaded", () => {

    updateSummary();

    renderAlerts(alertsData);

});


/* =========================================
   FILTER BUTTONS
========================================= */

document
    .querySelectorAll(".alert-filter")
    .forEach(button => {

        button.addEventListener("click", () => {

            document
                .querySelectorAll(".alert-filter")
                .forEach(item => {
                    item.classList.remove("active");
                });

            button.classList.add("active");

            currentFilter =
                button.dataset.filter;

            filterAlerts();

        });

    });


/* =========================================
   FILTER ALERTS
========================================= */

function filterAlerts() {

    let filteredAlerts;

    if (currentFilter === "all") {

        filteredAlerts =
            alertsData;

    } else {

        filteredAlerts =
            alertsData.filter(
                alert => alert.type === currentFilter
            );

    }

    renderAlerts(filteredAlerts);

}


/* =========================================
   RENDER ALERTS
========================================= */

function renderAlerts(alerts) {

    alertList.innerHTML = "";


    if (alerts.length === 0) {

        emptyAlerts.classList.remove("hidden");

        return;

    }


    emptyAlerts.classList.add("hidden");


    alerts.forEach(alert => {

        const alertItem =
            document.createElement("div");

        alertItem.className =
            `alert-item ${alert.unread ? "unread" : ""}`;


        const icon =
            getAlertIcon(alert.type);


        const typeLabel =
            getAlertTypeLabel(alert.type);


        alertItem.innerHTML = `

            <div class="alert-icon ${alert.type}">
                <i class="${icon}"></i>
            </div>


            <div class="alert-content">

                <h3>
                    ${alert.title}
                </h3>

                <p>
                    ${alert.message}
                </p>

                <div class="alert-meta">

                    <span>
                        <i class="fa-solid fa-clock"></i>
                        ${alert.date} ${alert.time}
                    </span>

                    <span>
                        <i class="fa-solid fa-hashtag"></i>
                        ${alert.eventId}
                    </span>

                </div>

            </div>


            <div class="alert-side">

                <span class="alert-type ${alert.type}">
                    ${typeLabel}
                </span>

                <a
                    href="earthquake.html?id=${alert.eventId}"
                    class="alert-view"
                >
                    View Event
                    <i class="fa-solid fa-arrow-right"></i>
                </a>

            </div>

        `;


        alertList.appendChild(alertItem);

    });

}


/* =========================================
   ALERT ICON
========================================= */

function getAlertIcon(type) {

    if (type === "high") {

        return "fa-solid fa-triangle-exclamation";

    }

    if (type === "moderate") {

        return "fa-solid fa-shield-halved";

    }

    return "fa-solid fa-circle-info";

}


/* =========================================
   ALERT TYPE LABEL
========================================= */

function getAlertTypeLabel(type) {

    if (type === "high") {
        return "High Risk";
    }

    if (type === "moderate") {
        return "Moderate";
    }

    return "Information";

}


/* =========================================
   UPDATE SUMMARY
========================================= */

function updateSummary() {

    const active =
        alertsData.filter(
            alert => alert.unread
        ).length;

    const highRisk =
        alertsData.filter(
            alert => alert.type === "high"
        ).length;


    activeAlertCount.textContent =
        active;

    highRiskCount.textContent =
        highRisk;

    recentEventCount.textContent =
        alertsData.length;

}


/* =========================================
   MARK ALL AS READ
========================================= */

markAllRead.addEventListener("click", () => {

    alertsData.forEach(alert => {

        alert.unread = false;

    });


    updateSummary();

    filterAlerts();


    markAllRead.innerHTML = `
        <i class="fa-solid fa-check"></i>
        All Alerts Read
    `;

});


/* =========================================
   FUTURE REAL-TIME ALERT INTEGRATION
========================================= */

/*
    Future architecture:

    Earthquake WebSocket
            ↓
       FastAPI Backend
            ↓
       alerts.js
            ↓
       New Alert UI

    Example future WebSocket message:

    {
        "event_id": "EMSC-20261012-001",
        "magnitude": 6.8,
        "region": "Panama",
        "risk": "high",
        "message": "High magnitude earthquake detected"
    }

    A new alert can then be inserted into
    alertsData and rendered immediately.
*/