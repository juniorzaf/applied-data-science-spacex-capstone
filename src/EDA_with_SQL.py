import csv, sqlite3
import prettytable
prettytable.DEFAULT = 'DEFAULT'

con = sqlite3.connect("my_data1.db")
cur = con.cursor()

import pandas as pd
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")

#Note:This below code is added to remove blank rows from table

#DROP THE TABLE IF EXISTS
%sql DROP TABLE IF EXISTS SPACEXTABLE;

%sql create table SPACEXTABLE as select * from SPACEXTBL where Date is not null

#Display the names of the unique launch sites in the space mission
%sql Select DISTINCT Launch_Site from SPACEXTABLE

#Display 5 records where launch sites begin with the string 'CCA'
%sql select * from SPACEXTABLE WHERE Launch_Site LIKE 'CCA%' LIMIT 5

#Display the total payload mass carried by boosters launched by NASA (CRS)
%sql select SUM(PAYLOAD_MASS__KG_) from SPACEXTABLE WHERE Customer='NASA (CRS)'

#Display average payload mass carried by booster version F9 v1.1
%sql SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEXTABLE WHERE Booster_Version LIKE '%F9 v1.1%'

#List the date when the first succesful landing outcome in ground pad was acheived.
%sql SELECT MIN(Date) FROM SPACEXTABLE WHERE Landing_Outcome LIKE 'Success (ground pad)'

#List the names of the boosters which have success in drone ship and have payload mass greater than 4000 but less than 6000
%sql select Booster_Version from SPACEXTABLE WHERE (Landing_Outcome LIKE 'Success (drone ship)') AND (PAYLOAD_MASS__KG_<6000 and PAYLOAD_MASS__KG_>4000)

#List the total number of successful and failure mission outcomes
%sql select  Mission_Outcome, count(*) as Total FROM SPACEXTABLE WHERE Mission_Outcome is not null GROUP BY Mission_Outcome

#List all the booster_versions that have carried the maximum payload mass, using a subquery with a suitable aggregate function.
%sql SELECT Booster_Version , PAYLOAD_MASS__KG_ FROM SPACEXTABLE WHERE PAYLOAD_MASS__KG_=(SELECT max(PAYLOAD_MASS__KG_) from SPACEXTABLE)

#List the records which will display the month names, failure landing_outcomes in drone ship ,booster versions, launch_site for the months in year 2015.
%sql select Case substr(Date,6,2) WHEN '01' THEN 'JANUARY' WHEN '02' THEN 'FEBRUARY' WHEN '03' THEN 'MARCH'WHEN '04' THEN 'April' WHEN '05' THEN 'May' WHEN '06' THEN 'June' WHEN '07' THEN 'July' WHEN '08' THEN 'August' WHEN '09' THEN 'September' WHEN '10' THEN 'October'  WHEN '11' THEN 'November' WHEN '12' THEN 'December' END AS Month_Name, Landing_Outcome, Booster_Version, Launch_Site FROM SPACEXTABLE WHERE SUBSTR(Date, 1, 4) = '2015' AND Landing_Outcome LIKE 'Failure (drone ship)%'

#Rank the count of landing outcomes (such as Failure (drone ship) or Success (ground pad)) between the date 2010-06-04 and 2017-03-20, in descending order.¶
%sql SELECT Landing_Outcome, COUNT(*) AS Outcome_Count FROM SPACEXTABLE WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY Outcome_Count DESC