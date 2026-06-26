# SpaceX Dataset Documentation

This directory contains the datasets collected, cleaned, and engineered throughout the SpaceX Falcon 9 landing prediction case study.

## 📂 Data Sources

The data used in this project was compiled from two main sources:

1. **SpaceX API:** Used to retrieve core operational data about past launches, including rocket features, payload details, launchpad locations, and the specific outcomes of the first-stage landings.
2. **Wikipedia Web Scraping:** Used to gather additional historical context and alternative launch records by parsing the official list of Falcon 9 launches.

---

## 📊 Dataset Dictionary

The final engineered dataset (`dataset_part_2.csv` or `dataset_part_3.csv`) used for the Machine Learning models includes the following key variables:

* **FlightNumber:** The sequential number of the launch.
* **Date:** The date of the launch (YYYY-MM-DD).
* **BoosterVersion:** The specific version/generation of the Falcon 9 booster.
* **PayloadMass:** The total mass of the payload carried into orbit (in kilograms).
* **Orbit:** The target orbit type (e.g., LEO, GTO, ISS, VLEO).
* **LaunchSite:** The location of the launch (e.g., CCAFS SLC 40, KSC LC 39A, VAFB SLC 4E).
* **Outcome:** The raw outcome of the landing attempt (e.g., True ASDS, False Ocean, None).
* **Flights:** The number of times this specific booster has flown.
* **GridFins:** Boolean (`True`/`False`) indicating if grid fins were used for landing control.
* **Reused:** Boolean indicating if the booster had been flown previously.
* **Legs:** Boolean indicating if landing legs were deployed.
* **LandingPad:** The specific drone ship or landing zone identifier.
* **Block:** The core block version of the missile/booster.
* **ReusedCount:** Total times this booster was successfully reused.
* **Serial:** The unique serial number of the booster core.
* **Longitude / Latitude:** Geographic coordinates of the launch site.
* **Class (Target Variable):** 
  * `1` = Successful first-stage landing.
  * `0` = Unsuccessful or landed landing attempt.

---

## ⚠️ Notes on Usage
The files in this folder are preprocessed and standardized during the script execution pipeline via `StandardScaler`. If you plan to rerun the raw data collection from scratch, please ensure your environment has an active internet connection to ping the SpaceX API.
