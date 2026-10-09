
from django.shortcuts import render
from .form import PredictionForm
import joblib
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.figure_factory as ff 
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
# Create your views here.

def analysis(request):
    df= pd.read_csv(os.path.join(BASE_DIR, "clean_data.csv"))
   
#year_rate
    year_rate = df["Year"].value_counts().sort_index()
    year_fig=px.line(x=year_rate.index,y=year_rate.values,labels={"x": "Year", "y": "Accidents"},title="Accidents rate by Year")

#month_rate
    def no_acc_month():
        jan_mar=0
        apr_jun=0
        jul_sep = 0
        oct_dec=0

        for i in df["Month"]:
            if i in ["January", "February", "March"]:
               jan_mar+=1
            elif i in ["April", "May", "June"]:
               apr_jun+=1
            elif i in ["July", "August", "September"]:
               jul_sep+=1
            elif i in ["October", "November", "December"]:
               oct_dec+=1 
        return jan_mar, apr_jun, jul_sep, oct_dec

    months=['Jan-Mar','Apr-Jun','Jul-Sep','Oct-Dec']
    monthly_rate=list(no_acc_month())

    month_fig = px.bar(x=months,y=monthly_rate,labels={"x": "Month", "y": "Accidents"},title="Montly accident rate")
    month_fig.update_layout(
        
    )
#hour rate   

    acc_time=pd.to_datetime(df["Time of Day"], format="mixed").dt.hour
    time_rate = acc_time.value_counts().sort_index()
    time_fig=px.line(x=time_rate.index,y=time_rate.values,labels={"x": "Hour", "y": "Accidents"},title="Accidents rate by Time of the day")

#alcohol pie
    alcohol_fig = px.pie(
        df,
        names="Alcohol Involvement",
        title="Alcohol Involvement in Accidents"
    )
   

#vehical/severity
    fig_severity = px.bar(
        df,
        y="Number of Vehicles Involved",
        x="Accident Location Details",
        color="Accident Severity",
        title="Number of Vehicles Involved by Accident Location",
        labels={
            "y": "Number of Vehicles Involved",
            "x": "Accident Location Details",
            "color":"Accident Severity",
        }
    )



#casualties
    casualties= (
        df.groupby("Vehicle Type Involved")["Total Number of Casualties"]
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

  # by state  
    state_accidents = df["State Name"].value_counts().reset_index()

    state_accidents.columns = ["State Name", "Number of Accidents"]

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

#severity heatmap
    severity_heatmap = pd.crosstab(
        df["Accident Severity"],
        df["Road Condition"]
    )

    road_fig = px.imshow(
    severity_heatmap,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Viridis",
    labels=dict(
    x="Road Condition",
    y="Accident Severity",
    color="Number of Accidents"
    ),
    title="Accident Severity by Road Condition"
    )

    
#by state / severity

    state_severity = pd.crosstab(
        df["State Name"],
        df["Accident Severity"]
    )

    fig_state= px.bar(
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
   
 
    return render(
        request,
        "accident/analysis.html",
        {
            "year_fig": year_fig.to_html(full_html=False),
            "month_fig": month_fig.to_html(full_html=False),
            "time_fig":time_fig.to_html(full_html=False),
            "alcohol_fig":alcohol_fig.to_html(full_html=False),
            "fig_severity":fig_severity.to_html(full_html=False),
            "casualties_fig":casualties_fig.to_html(full_html=False),
            "road_fig":road_fig.to_html(full_html=False),
            "state_fig":state_fig.to_html(full_html=False),
            "fig_state":fig_state.to_html(full_html=False),
        }
    )


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