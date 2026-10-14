document.addEventListener("DOMContentLoaded", () => {

    updateDateTime();

    setInterval(updateDateTime, 1000);

});


function updateDateTime() {

    const now = new Date();

    const timeElement =
        document.getElementById("currentTime");

    const dateElement =
        document.getElementById("currentDate");

    const lastUpdated =
        document.getElementById("lastUpdated");


    if (timeElement) {

        timeElement.textContent =
            now.toLocaleTimeString("en-IN", {
                hour12: false
            });

    }


    if (dateElement) {

        dateElement.textContent =
            now.toLocaleDateString("en-IN", {
                day: "2-digit",
                month: "short",
                year: "numeric"
            });

    }


    if (lastUpdated) {

        lastUpdated.textContent =
            now.toLocaleTimeString("en-IN", {
                hour12: false
            });

    }

}