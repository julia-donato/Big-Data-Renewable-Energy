# Impact Analysis of Socio-economic Factors on Renewable Energy Consumption

## Introduction
This report analyzes the interplay between socio-economic development and renewable energy consumption in emerging economies using data from World Data and the National Solar Radiation Database. The study focuses on Indonesia, China, India, South Africa, and Brazil to understand their transitions to sustainable energy practices.

## Methodology
- Data extracted from the National Solar Radiation Database using a Python script, `BigData_ETL.py`.
- GCP used for data processing; VMs and Google Cloud Storage were the primary infrastructure.
- World Data data preprocessed and stored in Google Bigtable; analysis performed using Jupyter notebooks.

## Results
- Analysis of Global Horizontal Irradiance (GHI) for the target countries.
- Trends in renewable energy consumption and their correlation with CO2 emissions, FDI, and PPP investments, etc. from 2012 to 2023.
- Assessment of socio-economic impacts on renewable energy consumption using Bigtable.

## Discussion
The project applied course-learned technologies like GCP and NoSQL databases. Challenges encountered included NoSQL database complexities and data interpretation issues.

## Conclusion
The project reveals how socio-economic factors influence renewable energy uptake in emerging economies and highlights the potential routes for sustainable development.

## Repository Contents
- `BigData_ETL.py`: Script for NSRDB data extraction
- `nosql_preprocess.py`: Script for World Bank data preprocessing
- `No_SQL_Database_Analysis.ipynb`: Jupyter notebook for World Bank data analysis
- `Course_Project_Report.pdf`: Project Report
- `EDA`: Exploratory analysis of NSRDB Data
- `World_Data.csv`: World Bank Open Data data
- `World_Data- Metadata.csv`: World Bank Open Data data
- `ETL_Output`: Folder containing metadata and images from VM ETL
- `README.md`: This document
For a detailed examination of the methodologies and findings, refer to the full report in this repository.
