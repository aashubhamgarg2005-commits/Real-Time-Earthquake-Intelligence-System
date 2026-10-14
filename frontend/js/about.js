/* =========================================
   ABOUT PAGE JAVASCRIPT
========================================= */

document.addEventListener("DOMContentLoaded", () => {

    initializeArchitectureInteraction();
    initializeScrollReveal();

});


/* =========================================
   ARCHITECTURE INTERACTION
========================================= */

function initializeArchitectureInteraction() {

    const architectureSteps =
        document.querySelectorAll(".architecture-step");

    architectureSteps.forEach((step, index) => {

        step.addEventListener("click", () => {

            architectureSteps.forEach(item => {
                item.classList.remove("selected");
            });

            step.classList.add("selected");

            console.log(
                `Architecture step selected: ${index + 1}`
            );

        });

    });

}


/* =========================================
   SIMPLE SCROLL REVEAL
========================================= */

function initializeScrollReveal() {

    const elements = document.querySelectorAll(
        ".info-card, " +
        ".architecture-step, " +
        ".technology-card, " +
        ".feature-card, " +
        ".team-card, " +
        ".objectives-card"
    );

    if (!("IntersectionObserver" in window)) {
        elements.forEach(element => {
            element.style.opacity = "1";
            element.style.transform = "translateY(0)";
        });

        return;
    }


    elements.forEach(element => {

        element.style.opacity = "0";
        element.style.transform = "translateY(15px)";
        element.style.transition =
            "opacity 0.5s ease, transform 0.5s ease";

    });


    const observer = new IntersectionObserver(
        (entries, observerInstance) => {

            entries.forEach(entry => {

                if (!entry.isIntersecting) {
                    return;
                }

                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";

                observerInstance.unobserve(entry.target);

            });

        },
        {
            threshold: 0.12
        }
    );


    elements.forEach(element => {
        observer.observe(element);
    });

}


/* =========================================
   FUTURE BACKEND INTEGRATION
========================================= */

/*
   About page normally does not require a backend API.

   If project information later becomes dynamic,
   this file can fetch information from FastAPI.

   Example future endpoint:

   GET /api/project-info

   Possible response:

   {
       "name": "Earthquake Intel",
       "version": "1.0",
       "status": "online",
       "data_source": "WebSocket",
       "streaming": "Kafka + Spark"
   }

   The frontend can then update the page dynamically.
*/