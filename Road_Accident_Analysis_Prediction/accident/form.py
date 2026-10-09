from django import forms


class PredictionForm(forms.Form):

    year = forms.IntegerField(label="Year")
    month = forms.ChoiceField(
        label="Month",
        choices=[
            ("January", "January"),
            ("February", "February"),
            ("March", "March"),
            ("April", "April"),
            ("May", "May"),
            ("June", "June"),
            ("July", "July"),
            ("August", "August"),
            ("September", "September"),
            ("October", "October"),
            ("November", "November"),
            ("December", "December"),
        ]
    )

    day = forms.ChoiceField(
        label="Day of Week",
        choices=[
            ("Monday", "Monday"),
            ("Tuesday", "Tuesday"),
            ("Wednesday", "Wednesday"),
            ("Thursday", "Thursday"),
            ("Friday", "Friday"),
            ("Saturday", "Saturday"),
            ("Sunday", "Sunday"),
        ]
    )

    
    hour = forms.IntegerField(
        label="Hour",
        min_value=0,
        max_value=23
    )

    vehicles = forms.IntegerField(
        label="Number of Vehicles Involved"
    )

    vehicle_type = forms.ChoiceField(
        label="Vehicle Type",
        choices=[
            ("Auto-Rickshaw", "Auto-Rickshaw"),
            ("Bus", "Bus"),
            ("Car", "Car"),
            ("Cycle", "Cycle"),
            ("Pedestrian", "Pedestrian"),
            ("Truck", "Truck"),
            ("Two-Wheeler", "Two-Wheeler"),
        ]
    )

    speed_limit = forms.IntegerField(
        label="Speed Limit (km/h)"
    )


    casualties = forms.IntegerField(
        label="Total Number of Casualties"
    )

    state = forms.ChoiceField(
        label="State",
        choices=[
            ("Andhra Pradesh", "Andhra Pradesh"),
            ("Arunachal Pradesh", "Arunachal Pradesh"),
            ("Assam", "Assam"),
            ("Bihar", "Bihar"),
            ("Chandigarh", "Chandigarh"),
            ("Chhattisgarh", "Chhattisgarh"),
            ("Delhi", "Delhi"),
            ("Goa", "Goa"),
            ("Gujarat", "Gujarat"),
            ("Haryana", "Haryana"),
            ("Himachal Pradesh", "Himachal Pradesh"),
            ("Jammu and Kashmir", "Jammu and Kashmir"),
            ("Jharkhand", "Jharkhand"),
            ("Karnataka", "Karnataka"),
            ("Kerala", "Kerala"),
            ("Madhya Pradesh", "Madhya Pradesh"),
            ("Maharashtra", "Maharashtra"),
            ("Manipur", "Manipur"),
            ("Meghalaya", "Meghalaya"),
            ("Mizoram", "Mizoram"),
            ("Nagaland", "Nagaland"),
            ("Odisha", "Odisha"),
            ("Puducherry", "Puducherry"),
            ("Punjab", "Punjab"),
            ("Rajasthan", "Rajasthan"),
            ("Sikkim", "Sikkim"),
            ("Tamil Nadu", "Tamil Nadu"),
            ("Telangana", "Telangana"),
            ("Tripura", "Tripura"),
            ("Uttar Pradesh", "Uttar Pradesh"),
            ("Uttarakhand", "Uttarakhand"),
            ("West Bengal", "West Bengal"),
        ]
    )



    weather = forms.ChoiceField(
        label="Weather Conditions",
        choices=[
            ("Clear", "Clear"),
            ("Foggy", "Foggy"),
            ("Hazy", "Hazy"),
            ("Rainy", "Rainy"),
            ("Stormy", "Stormy"),
        ]
    )



    road_condition = forms.ChoiceField(
        label="Road Condition",
        choices=[
            ("Damaged", "Damaged"),
            ("Dry", "Dry"),
            ("Under Construction", "Under Construction"),
            ("Wet", "Wet"),
        ]
    )


   
    license_status = forms.ChoiceField(
        label="Driving License Status",
        choices=[
            ("Expired", "Expired"),
            ("Not Available", "Not Available"),
            ("Valid", "Valid"),
        ]
    )

    location = forms.ChoiceField(
        label="Accident Location Details",
        choices=[
            ("Bridge", "Bridge"),
            ("Curve", "Curve"),
            ("Intersection", "Intersection"),
            ("Straight Road", "Straight Road"),
        ]
    )

    alcohol = forms.ChoiceField(
        label="Alcohol Involvement",
        choices=[
            ("No", "No"),
            ("Yes", "Yes"),
        ]
    )
