from pathlib import Path

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

import joblib
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "https://codingwithvivek22.github.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
scaler = joblib.load(BASE_DIR / "../model/scaler.pkl")

with open(BASE_DIR / "../model/feature_columns.json", "r") as f:
    feature_columns = json.load(f)

import torch
import torch.nn as nn

class ANN(nn.Module):

    def __init__(self, input_size):
        super().__init__()

        self.model = nn.Sequential(

            nn.Linear(input_size, 64),
            nn.ReLU(),

            nn.Linear(64, 32),
            nn.ReLU(),

            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):

        return self.model(x)

model = ANN(len(feature_columns))

model.load_state_dict(
    torch.load(BASE_DIR / "../model/ann_model.pth", map_location="cpu")
)

model.eval()


@app.get("/")
def home():
    return {"message" : "Customer Churn API is Running"}


class Customer(BaseModel):

    gender: int
    SeniorCitizen: int
    Partner: int
    Dependents: int
    tenure: float
    PhoneService: int
    MultipleLines: int
    OnlineSecurity: int
    OnlineBackup: int
    DeviceProtection: int
    TechSupport: int
    StreamingTV: int
    StreamingMovies: int
    Contract: Literal[
        "Month-to-month",
        "One year",
        "Two year"
    ]
    PaperlessBilling: int

    MonthlyCharges: float
    TotalCharges: float

    InternetService: Literal[

        "DSL",
        "Fiber optic",
        "No"
    ]

    PaymentMethod: Literal[

        "Bank transfer (automatic)",
        "Credit card (automatic)",
        "Electronic check",
        "Mailed check"
    ]

@app.post("/predict")
def predict(customer: Customer):

    import pandas as pd

    data = customer.model_dump()
    df = pd.DataFrame([data])

    df = pd.get_dummies(
        df, 
        columns=["InternetService", "PaymentMethod", "Contract"]
    )

    df = df.reindex(
        columns = feature_columns,
        fill_value = 0
    )

    scaled_data = scaler.transform(df)

    X = torch.FloatTensor(scaled_data)

    with torch.no_grad():
        output = model(X)

    prediction = (output > 0.5).float()

    return {

        "churn_probability" : output.item(),
        "prediction" : int(prediction.item())
    }
    
    

    