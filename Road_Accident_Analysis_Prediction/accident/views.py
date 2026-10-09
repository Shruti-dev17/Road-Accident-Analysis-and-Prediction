
from django.shortcuts import render
from .form import PredictionForm
import joblib
import pandas as pd
import plotly.express as px
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
# Create your views here.


def analysis(request):
    df = pd.read_csv(os.path.join(BASE_DIR, "clean_data.csv"))

    # by year
    year_rate = df["Year"].value_counts().sort_index()

    year_fig = px.line(
        x=year_rate.index,
        y=year_rate.values,
        labels={"x": "Year", "y": "Accidents"},
        title="Accidents by Year",
        markers=True
    )

    # by quarter
    month_groups = {
        "Jan-Mar": ["January", "February", "March"],
        "Apr-Jun": ["April", "May", "June"],
        "Jul-Sep": ["July", "August", "September"],
        "Oct-Dec": ["October", "November", "December"],
    }

    monthly_rate = [
        df["Month"].isin(months).sum()
        for months in month_groups.values()
    ]

    month_fig = px.bar(
        x=list(month_groups.keys()),
        y=monthly_rate,
        labels={"x": "Month", "y": "Accidents"},
        title="Accidents by Quarter"
    )

    # by time of day
    acc_time = pd.to_datetime(
        df["Time of Day"], format="mixed"
    ).dt.hour

    time_rate = acc_time.value_counts().sort_index()

    time_fig = px.line(
        x=time_rate.index,
        y=time_rate.values,
        labels={"x": "Hour", "y": "Accidents"},
        title="Accidents by Time of Day",
        markers=True
    )

    # 4. Alcohol involvement
    alcohol_data = (
        df["Alcohol Involvement"]
        .value_counts(dropna=False)
        .reset_index()
    )
    alcohol_data.columns = ["Alcohol Involvement", "Count"]

    alcohol_fig = px.pie(
        alcohol_data,
        names="Alcohol Involvement",
        values="Count",
        title="Alcohol Involvement in Accidents"
    )

    # Vehicles involved by location and severity
    severity_data = (
        df.groupby(
            ["Accident Location Details", "Accident Severity"],
            as_index=False,
            dropna=False
        )["Number of Vehicles Involved"]
        .sum()
    )

    fig_severity = px.bar(
        severity_data,
        x="Accident Location Details",
        y="Number of Vehicles Involved",
        color="Accident Severity",
        title="Vehicles Involved by Location and Severity",
        labels={
            "y": "Number of Vehicles Involved",
            "x": "Accident Location",
            "color": "Accident Severity",
        }
    )

    #Average casualties by vehicle type
    casualties = (
        df.groupby("Vehicle Type Involved")[
            "Total Number of Casualties"
        ]
        .mean()
        .reset_index()
    )

    casualties_fig = px.line(
        casualties,
        x="Vehicle Type Involved",
        y="Total Number of Casualties",
        title="Average Casualties by Vehicle Type",
        markers=True
    )

    #Accidents by state
    state_accidents = (
        df["State Name"]
        .value_counts()
        .rename_axis("State Name")
        .reset_index(name="Number of Accidents")
    )

    state_fig = px.bar(
        state_accidents,
        x="State Name",
        y="Number of Accidents",
        title="Accidents by State",
        labels={
            "State Name": "State",
            "Number of Accidents": "Number of Accidents"
        }
    )

    #Severity by road condition
    severity_heatmap = pd.crosstab(
        df["Accident Severity"],
        df["Road Condition"]
    )

    road_fig = px.imshow(
        severity_heatmap,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Viridis",
        labels={
            "x": "Road Condition",
            "y": "Accident Severity",
            "color": "Number of Accidents"
        },
        title="Accident Severity by Road Condition"
    )

    # State-wise accident severity
    state_severity = pd.crosstab(
        df["State Name"],
        df["Accident Severity"]
    )

    fig_state = px.bar(
        state_severity,
        x=state_severity.index,
        y=state_severity.columns,
        title="State-wise Accident Severity",
        labels={
            "x": "State",
            "value": "Number of Accidents",
            "variable": "Accident Severity"
        }
    )

 
    charts = {
        "year_fig": year_fig,
        "month_fig": month_fig,
        "time_fig": time_fig,
        "alcohol_fig": alcohol_fig,
        "fig_severity": fig_severity,
        "casualties_fig": casualties_fig,
        "road_fig": road_fig,
        "state_fig": state_fig,
        "fig_state": fig_state,
    }

    context = {
        name: fig.to_html(
            full_html=False,
            include_plotlyjs=False,
            config={"displayModeBar": False}
        )
        for name, fig in charts.items()
    }

    return render(request, "accident/analysis.html", context)

importance = pd.read_csv(os.path.join(BASE_DIR, "models", "feature_importance.csv"))
cm = joblib.load(os.path.join(BASE_DIR, "models", "confusion_matrix.pkl"))
class_labels = joblib.load(os.path.join(BASE_DIR, "models", "class_labels.pkl"))
    
def evaluation(request):
    importance_fig = px.bar(
            importance.sort_values("Importance"),
            x="Importance",
            y="Feature",
            orientation="h",
            title="Top 10 Features Used by the Model"
        )
    importance_fig.update_layout(height=500)
    
    cm_fig = px.imshow(
            cm,
            text_auto=True,
            x=class_labels,
            y=class_labels,
            color_continuous_scale="Blues",
            labels={
                "x": "Predicted Severity",
                "y": "Actual Severity",
                "color": "Count"
            },
            title="Confusion Matrix - Accident Severity"
        )
    return render(request,"accident/evaluation.html",
            {
                "importance_fig": importance_fig.to_html(full_html=False),
                "cm_fig": cm_fig.to_html(full_html=False)
            }
        )



model = joblib.load(os.path.join(BASE_DIR, "models", "accident_severity_model.pkl"))
feature_names = joblib.load(os.path.join(BASE_DIR, "models", "feature_names.pkl"))

def predict(request):
    prediction = None
    prediction_description = None

    if request.method == "POST":
        form = PredictionForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data

            # Start with all 96 features set to 0
            input_data = pd.DataFrame(
                0,
                index=[0],
                columns=feature_names
            )

            # Numerical features
            input_data["Year"] = data["year"]
            input_data["Number of Vehicles Involved"] = data["vehicles"]
            input_data["Speed Limit (km/h)"] = data["speed_limit"]
            input_data["Total Number of Casualties"] = data["casualties"]
            input_data["Hour"] = data["hour"]

            # Categorical features
            input_data["Month_" + data["month"]] = 1
            input_data["State Name_" + data["state"]] = 1
            input_data["Day of Week_" + data["day"]] = 1
            input_data["Vehicle Type Involved_" + data["vehicle_type"]] = 1
            input_data["Weather Conditions_" + data["weather"]] = 1
            input_data["Road Condition_" + data["road_condition"]] = 1
            input_data["Driver License Status_" + data["license_status"]] = 1
            input_data["Accident Location Details_" + data["location"]] = 1
            input_data["Alcohol Involvement_" + data["alcohol"]] = 1

           
            prediction = model.predict(input_data)[0]
            
            probabilities = model.predict_proba(input_data)[0]

            prediction_probabilities = {
                label: round(float(probability) * 100, 2)
                for label, probability in zip(model.classes_, probabilities)
            }
            severity_descriptions = {
                "Minor": "The model predicts a minor accident.",
                "Serious": "The model predicts a serious accident requiring greater attention.",
                "Fatal": "The model predicts a fatal accident outcome."
            }

            prediction_description = severity_descriptions.get(
                prediction,
                "Prediction completed."
            )

    else:
        form = PredictionForm()

 
    return render(
         request,
         "accident/index.html",
         {
             "form": form,
             "prediction": prediction,
             "prediction_description": prediction_description if prediction else None,
             "prediction_probabilities": prediction_probabilities if prediction else None,
         }
     )