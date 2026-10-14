/* =========================================
   AI ANALYSIS PAGE
========================================= */


/* =========================================
   AI EVENT DATA
   Temporary data for frontend testing.
   Later replace with FastAPI / ML API data.
========================================= */

const aiEvents = {

    panama: {

        id: "EMSC-20261012-001",

        region: "Panama",

        magnitude: 6.8,

        depth: 10,

        riskScore: 68,

        riskLevel: "Moderate Risk",

        magnitudeConfidence: 91,

        aftershockProbability: 64,

        summaryTitle:
            "Moderate Seismic Risk Detected",

        summaryText:
            "The current earthquake shows significant seismic energy. Based on magnitude, depth, location and historical patterns, the event requires continued monitoring.",

        depthStatus:
            "Shallow Earthquake",

        locationInsight:
            "The event location indicates a potentially significant seismic zone and should remain under observation.",

        depthInsight:
            "The shallow depth increases the possibility of stronger surface-level shaking near the epicenter.",

        historicalInsight:
            "Historical seismic patterns indicate that events of similar characteristics may require continued monitoring.",

        actionInsight:
            "Continue monitoring the event and follow official emergency guidance."

    },


    japan: {

        id: "EMSC-20261012-002",

        region: "Japan",

        magnitude: 5.7,

        depth: 42,

        riskScore: 54,

        riskLevel: "Moderate Risk",

        magnitudeConfidence: 88,

        aftershockProbability: 48,

        summaryTitle:
            "Moderate Seismic Activity",

        summaryText:
            "The event has moderate magnitude with an intermediate depth. AI analysis recommends continued observation of aftershock activity.",

        depthStatus:
            "Intermediate Depth",

        locationInsight:
            "The event occurred in a region with frequent seismic activity.",

        depthInsight:
            "Intermediate depth may reduce direct surface shaking compared with a shallow event.",

        historicalInsight:
            "Historical activity in the region suggests that aftershock monitoring is important.",

        actionInsight:
            "Monitor subsequent events and remain aware of local emergency information."

    },


    india: {

        id: "EMSC-20261012-003",

        region: "Himachal Pradesh, India",

        magnitude: 4.6,

        depth: 18,

        riskScore: 39,

        riskLevel: "Low Risk",

        magnitudeConfidence: 86,

        aftershockProbability: 31,

        summaryTitle:
            "Low to Moderate Seismic Activity",

        summaryText:
            "The event is relatively moderate in magnitude. AI analysis indicates lower immediate risk but recommends continued seismic monitoring.",

        depthStatus:
            "Shallow Earthquake",

        locationInsight:
            "The event occurred in a seismically active Himalayan region.",

        depthInsight:
            "The relatively shallow depth may increase localized ground shaking.",

        historicalInsight:
            "Historical seismic activity in the Himalayan region suggests continued monitoring is useful.",

        actionInsight:
            "Monitor for additional seismic events and follow local authority guidance."

    }

};


/* =========================================
   DOM ELEMENTS
========================================= */

const eventSelect =
    document.getElementById("eventSelect");

const eventRegion =
    document.getElementById("eventRegion");

const eventId =
    document.getElementById("eventId");

const riskScore =
    document.getElementById("riskScore");

const riskLevel =
    document.getElementById("riskLevel");

const predictedMagnitude =
    document.getElementById("predictedMagnitude");

const magnitudeConfidence =
    document.getElementById("magnitudeConfidence");

const magnitudeConfidenceText =
    document.getElementById("magnitudeConfidenceText");

const depthValue =
    document.getElementById("depthValue");

const depthStatus =
    document.getElementById("depthStatus");

const aftershockProbability =
    document.getElementById("aftershockProbability");

const aftershockBar =
    document.getElementById("aftershockBar");

const aiSummaryTitle =
    document.getElementById("aiSummaryTitle");

const aiSummaryText =
    document.getElementById("aiSummaryText");

const locationInsight =
    document.getElementById("locationInsight");

const depthInsight =
    document.getElementById("depthInsight");

const historicalInsight =
    document.getElementById("historicalInsight");

const actionInsight =
    document.getElementById("actionInsight");


/* =========================================
   INITIALIZE
========================================= */

document.addEventListener("DOMContentLoaded", () => {

    updateAnalysis("panama");

});


/* =========================================
   EVENT CHANGE
========================================= */

eventSelect.addEventListener("change", () => {

    updateAnalysis(eventSelect.value);

});


/* =========================================
   UPDATE AI ANALYSIS
========================================= */

function updateAnalysis(eventKey) {

    const event =
        aiEvents[eventKey];

    if (!event) {
        return;
    }


    /* Basic information */

    eventRegion.textContent =
        event.region;

    eventId.textContent =
        event.id;


    /* Risk */

    riskScore.textContent =
        event.riskScore;

    riskLevel.textContent =
        event.riskLevel;


    updateRiskCircle(event.riskScore);


    /* Magnitude */

    predictedMagnitude.textContent =
        event.magnitude.toFixed(1);

    magnitudeConfidence.style.width =
        `${event.magnitudeConfidence}%`;

    magnitudeConfidenceText.textContent =
        `${event.magnitudeConfidence}%`;


    /* Depth */

    depthValue.textContent =
        event.depth;

    depthStatus.textContent =
        event.depthStatus;


    /* Aftershock */

    aftershockProbability.textContent =
        event.aftershockProbability;

    aftershockBar.style.width =
        `${event.aftershockProbability}%`;


    /* AI summary */

    aiSummaryTitle.textContent =
        event.summaryTitle;

    aiSummaryText.textContent =
        event.summaryText;


    /* Insights */

    locationInsight.textContent =
        event.locationInsight;

    depthInsight.textContent =
        event.depthInsight;

    historicalInsight.textContent =
        event.historicalInsight;

    actionInsight.textContent =
        event.actionInsight;

}


/* =========================================
   RISK CIRCLE
========================================= */

function updateRiskCircle(score) {

    const circle =
        document.querySelector(".risk-circle");

    if (!circle) {
        return;
    }


    circle.style.background = `
        radial-gradient(
            circle,
            #ffffff 57%,
            transparent 58%
        ),
        conic-gradient(
            #168fff ${score}%,
            #e7edf2 0
        )
    `;


    const riskDot =
        document.querySelector(".risk-dot");

    if (riskDot) {

        if (score >= 70) {
            riskDot.style.background = "#d44c4c";
        }

        else if (score >= 40) {
            riskDot.style.background = "#e3a21a";
        }

        else {
            riskDot.style.background = "#1eb875";
        }

    }

}


/* =========================================
   FUTURE API INTEGRATION
========================================= */

/*
    Future architecture:

    FastAPI
       ↓
    ML/DL Prediction API
       ↓
    ai-analysis.js
       ↓
    Update UI

    Example future response:

    {
        "event_id": "...",
        "risk_score": 72,
        "aftershock_probability": 67,
        "predicted_magnitude": 6.9,
        "confidence": 93
    }

    Then this page can display real
    model predictions instead of mock data.
*/