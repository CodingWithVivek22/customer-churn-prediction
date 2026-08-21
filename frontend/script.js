const form = document.getElementById("predictionForm");

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    console.log("BUTTON CLICKED");

    const customerData = {

        gender: Number(document.getElementById("gender").value),

        SeniorCitizen: Number(
            document.getElementById("SeniorCitizen").value
        ),

        Partner: Number(
            document.getElementById("Partner").value
        ),

        Dependents: Number(
            document.getElementById("Dependents").value
        ),

        tenure: Number(
            document.getElementById("tenure").value
        ),

        PhoneService: Number(
            document.getElementById("PhoneService").value
        ),

        MultipleLines: Number(
            document.getElementById("MultipleLines").value
        ),

        OnlineSecurity: Number(
            document.getElementById("OnlineSecurity").value
        ),

        OnlineBackup: Number(
            document.getElementById("OnlineBackup").value
        ),

        DeviceProtection: Number(
            document.getElementById("DeviceProtection").value
        ),

        TechSupport: Number(
            document.getElementById("TechSupport").value
        ),

        StreamingTV: Number(
            document.getElementById("StreamingTV").value
        ),

        StreamingMovies: Number(
            document.getElementById("StreamingMovies").value
        ),

        Contract: document.getElementById("Contract").value,

        PaperlessBilling: Number(
            document.getElementById("PaperlessBilling").value
        ),

        MonthlyCharges: Number(
            document.getElementById("MonthlyCharges").value
        ),

        TotalCharges: Number(
            document.getElementById("TotalCharges").value
        ),

        InternetService:
            document.getElementById("InternetService").value,

        PaymentMethod:
            document.getElementById("PaymentMethod").value
    };

    const API_URL =
        window.location.hostname === "localhost" ||
            window.location.hostname === "127.0.0.1"
            ? "http://127.0.0.1:8000"
            : "https://customer-churn-prediction-exkn.onrender.com";

    try {

        const response = await fetch(`${API_URL}/predict`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(customerData)

        });

        const result = await response.json();

        console.log(result);

        document.getElementById("result").innerHTML = `
    <h2>Prediction Result</h2>
    <p>Churn Probability: ${(result.churn_probability * 100).toFixed(2)}%</p>
    <p>Prediction: ${result.prediction === 1 ? "Churn" : "No Churn"}</p>
`;

    } catch (error) {

        console.error("Error:", error);

    }

});