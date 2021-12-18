# U.S. Medical Insurance Costs


## Description

This project has been suggested by Codecademy as a group project of Data Scientist Path in order to give us an opportunity to connect with other learners, to put in practice our skills acquired so far and to search and apply the newers.

## Source

The data we are using is collected in a csv file named insurance.csv and provided by [Codecademy](https://www.codecademy.com/paths/data-science/tracks/dscp-python-portfolio-project/modules/dscp-group-project-u-s-medical-insurance-costs/informationals/dscp-group-project-u-s-medical-insurance-costs).

## Dataset

Our dataset contains ```1338 rows``` of information about U.S. medical insurance costs of patients. This dataset is provided as ```insurance.csv``` file that has different type of attributs as sex, age, bmi, children, smoker, region, and charges. It is important to note we don't know how the data have been collected. Therefore, we don't know exactly the relationship between the variable attributs, but I can study the data satistically and infer the analysis.
![dataset](dataset_2021-12-18_154347.png)

## Goal

Our goal is based on the statistically view of the data. Therefore, our goal is to able to:
- to calculate the average age of the patients
- to globally calculate average insurance cost in the insurance data.
- to calculate the portion of males versus females in the insurance data.
- to have an insight on the cheapest and the most expensive insurance costs.
- to define a confidence interval of 95% for the insurance charges.
- to buid a dictionary with all patients information
- to categorize the patients insurance expenditures by region, by sex, and so forth.

## Actions

The first action we took is to acquire the from our given source. For that purpose we used  the helper function of loading csv file provided by Codecademy to load our data. But, as  the data in the insurance.csv file is organized in a tabular way where columns have same number of rows, each column header will represent an attribut variable that will be defined as a list variable so that we can import information in the form of python lists.

The second action consists of manipulating the data in order to fulfil adequately our goal. 