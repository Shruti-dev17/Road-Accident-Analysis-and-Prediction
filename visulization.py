import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import plotly.figure_factory as ff 
df= pd.read_csv(r"F:\Desktop\code\Road Accident Analysis And Prediction\clean_data.csv")

# yearly accident
year_rate = df["Year"].value_counts().sort_index()
year_fig=px.line(x=year_rate.index,y=year_rate.values,labels={"x": "Year", "y": "Accidents"},title="Accidents by Year")
year_fig.show()
# 3 month graph
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
month_fig.show()

# time of day
acc_time=pd.to_datetime(df["Time of Day"], format="mixed").dt.hour
time_rate = acc_time.value_counts().sort_index()
time_fig=px.line(x=time_rate.index,y=time_rate.values,labels={"x": "Hour", "y": "Accidents"},title="Accidents by Time of the day")
time_fig.show()

#alcohol involvement
alcohol_fig = px.pie(
    df,
    color=['y','b'],
    names="Alcohol Involvement",
    title="Alcohol Involvement in Accidents"
)

alcohol_fig.show()

#Accident location/severity
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

fig_severity.show()

#casualties/type of vehical

casualties= (
    df.groupby("Vehicle Type Involved")["Total Number of Casualties"]
    .mean()
    .reset_index()
)

casualties_fig1 = px.line(
    casualties,
    x="Vehicle Type Involved",
    y="Total Number of Casualties",
    title="Average Casualties by Vehicle Type",
    markers=True
)

casualties_fig1.show()

#state accident 
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

state_fig.show()


#road vs severity

severity_heatmap = pd.crosstab(
    df["Accident Severity"],
    df["Road Condition"]
)

road_fig = ff.create_annotated_heatmap(
    z=severity_heatmap.values,
    x=severity_heatmap.columns.tolist(),
    y=severity_heatmap.index.tolist(),
    annotation_text=severity_heatmap.values.astype(str),
    colorscale="Viridis"
)

road_fig.update_layout(
    title="Accident Severity vs Road Condition",
    xaxis_title="Road Condition",
    yaxis_title="Accident Severity"
)

road_fig.show()

# state/severity
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



fig_state.show()