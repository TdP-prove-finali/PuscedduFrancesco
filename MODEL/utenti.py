from dataclasses import dataclass

@dataclass
class Utente:
    User_ID: int
    age: int
    gender: str
    country: str
    Daily_Social_Media_Hours: float
    Daily_Entertainment_Hours: float
    Social_Media_Platforms_Used: int
    Primary_Platform: str
    Daily_Messaging_Hours: float
    Daily_Video_Content_Hours: float
    Daily_Gaming_Hours: float
    occupation: float
    Marital_Status: float
    Monthly_Income_USD: float
    Device_Type: float
    Internet_Speed_Mbps: float
    Subscription_Platforms: int
    Average_Sleep_Hours: float
    Physical_activity_Hours: float
    Reading_Hours: float
    Work_or_Study_Hours: float
    Screen_Hours: float
    Notifications_Received_Daily: int
    Daily_Music_Listening_Hours: float
    Preferred_Content_Type: str
    Primary_Social_Media_Goal: str
    Preferred_Entertainment_Platform: str
    Hours_Spent_in_Online_Communities: float
    Social_Media_Fatigue_Level: int
    News_Consumption_Hours: float
    Ad_Interaction_Count: int
    Hours_on_Educational_Platforms: float
    Parental_Status: str
    Tech_Savviness_Level: int
    Preferred_Device_for_Entertainment: str
    Data_Plan_Used: str
    Digital_Wellbeing_Awareness: str
    Sleep_Quality: int
    Social_Isolation_Feeling: int
    Monthly_Expenditure_on_Entertainment_USD: float
    # Social Media Fatigue level, tech savviness level, sleep quality, social isolation feeling
    # Are all classified on a scale from 1 to 10 --> (scale 1-10)#