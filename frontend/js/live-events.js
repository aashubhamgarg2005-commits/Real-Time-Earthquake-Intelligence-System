/* =====================================================
   LIVE EVENTS PAGE JAVASCRIPT
   ===================================================== */


/* ================= ELEMENTS ================= */

const filterButtons =
    document.querySelectorAll(".filter-btn");

const events =
    document.querySelectorAll(".live-event");

const eventCount =
    document.getElementById("eventCount");

const mapEventCount =
    document.getElementById("mapEventCount");

const fullscreenBtn =
    document.getElementById("fullscreenBtn");

const liveMap =
    document.getElementById("liveMap");


/* ================= FILTER EVENTS ================= */

filterButtons.forEach(button => {

    button.addEventListener("click", () => {

        const filter =
            button.dataset.filter;


        /* Remove active */

        filterButtons.forEach(btn => {

            btn.classList.remove("active");

        });


        /* Add active */

        button.classList.add("active");


        let visibleEvents = 0;


        /* Filter */

        events.forEach(item => {

            const eventType =
                item.dataset.type;


            if (
                filter === "all" ||
                eventType === filter
            ) {

                item.style.display = "grid";

                visibleEvents++;

            } else {

                item.style.display = "none";

            }

        });


        /* Update count */

        if (eventCount) {

            eventCount.textContent =
                visibleEvents;

        }

    });

});


/* ================= FULLSCREEN ================= */

if (fullscreenBtn) {

    fullscreenBtn.addEventListener(
        "click",
        () => {

            if (!document.fullscreenElement) {

                liveMap.requestFullscreen();

            } else {

                document.exitFullscreen();

            }

        }
    );

}


/* ================= MAP MARKERS ================= */

const markers =
    document.querySelectorAll(".live-marker");


markers.forEach(marker => {

    marker.addEventListener(
        "click",
        () => {

            const information =
                marker.getAttribute("title");

            if (information) {

                alert(
                    "Earthquake Event\n\n" +
                    information
                );

            }

        }
    );

});


/* ================= SIMULATE LIVE COUNTER ================= */

/*
    Abhi sirf UI testing ke liye hai.

    Later:

    FastAPI
       ↓
    WebSocket
       ↓
    This JavaScript
       ↓
    New earthquake
       ↓
    Add event + marker
*/


function simulateLiveEvent() {

    if (!mapEventCount) {
        return;
    }


    let current =
        parseInt(
            mapEventCount.textContent
        );


    /*
        Real project me yahan
        fake increment nahi hoga.

        WebSocket se actual event
        receive hoga.
    */

    current += 1;


    mapEventCount.textContent =
        current;

}


/*
    Testing ke liye 15 sec me
    counter update ho raha hai.

    Backend connect karne ke baad
    ise remove kar denge.
*/

const simulationTimer =
    setInterval(
        simulateLiveEvent,
        15000
    );


/* ================= WEBSOCKET READY ================= */

/*
    Future WebSocket structure:

    const socket =
        new WebSocket(
            "ws://127.0.0.1:8000/ws/earthquakes"
        );

    socket.onopen = () => {
        console.log("WebSocket connected");
    };

    socket.onmessage = (event) => {

        const earthquake =
            JSON.parse(event.data);

        console.log(
            "New earthquake:",
            earthquake
        );

        // Add new event to UI
        // Add marker to map
    };

    socket.onclose = () => {
        console.log("WebSocket disconnected");
    };
*/


/* ================= CONNECTION UI ================= */

function setConnectionStatus(connected) {

    const connectionBox =
        document.querySelector(
            ".connection-box"
        );


    if (!connectionBox) {
        return;
    }


    const dot =
        connectionBox.querySelector(
            "span:first-child"
        );

    const text =
        connectionBox.querySelector(
            ".connection-text"
        );


    if (connected) {

        dot.style.background =
            "#00c98b";

        dot.style.boxShadow =
            "0 0 8px #00c98b";

        text.textContent =
            "WebSocket Connected";

    } else {

        dot.style.background =
            "#ff4052";

        dot.style.boxShadow =
            "0 0 8px #ff4052";

        text.textContent =
            "WebSocket Disconnected";

    }

}


/* Initial UI state */

setConnectionStatus(true);