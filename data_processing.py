import pandas as pd 
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

raw_data = pd.read_csv(os.path.join(BASE_DIR, "accident_prediction_india.csv"))
df= raw_data.fillna("Not Available")
df["Total Number of Casualties"]= df["Number of Casualties"]+df["Number of Fatalities"]
df=df.drop("City Name",axis=1)
df=df.drop("Lighting Conditions",axis=1)
df=df.drop("Road Type",axis=1)
df=df.drop("Driver Gender",axis=1)
df=df.drop("Driver Age",axis=1)
df=df.drop("Traffic Control Presence",axis=1)
df=df.drop("Number of Casualties",axis=1)
df=df.drop("Number of Fatalities",axis=1)


df_ml= pd.get_dummies(df, columns=["Month",
                                "State Name",
                                "Day of Week",
                                "Vehicle Type Involved",
                                "Weather Conditions",
                                "Road Condition",
                                "Accident Location Details",
                                "Driver License Status",
                                "Alcohol Involvement"])  

df_ml["Hour"] = pd.to_datetime(df["Time of Day"], format="mixed").dt.hour


df.to_csv("clean_data.csv")
df_ml.to_csv("data_ML.csv")
