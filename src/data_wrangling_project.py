# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np

#Load Space X dataset
df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")

#Identify and calculate the percentage of the missing values in each attribute
df.isnull().sum()/len(df)*100

#Identify which columns are numerical and categorical:
df.dtypes

#Calculate the number of launches on each site
df['LaunchSite'].value_counts()

#Calculate the number and occurrence of each orbit
df['Orbit'].value_counts()

#Calculate the number and occurence of mission outcome of the orbits
landing_outcomes=df['Outcome'].value_counts()
for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)

#We create a set of outcomes where the second stage did not land successfully
bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])
bad_outcomes

#Create a landing outcome label from Outcome column
#Using the Outcome, create a list where the element is zero if the corresponding row in Outcome is in the set bad_outcome; otherwise, it's one. Then assign it to the variable landing_class
# landing_class = 0 if bad_outcome
# landing_class = 1 otherwise
landing_class=[ 0 if outcome in bad_outcomes else 1 for outcome in df['Outcome']]

df['Class']=landing_class
df[['Class']].head(8)

df["Class"].mean()