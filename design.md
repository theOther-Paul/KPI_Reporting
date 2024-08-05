# Design Sheet for the application

## Layout
A 2 container app, with a sidebar and a main container that shows the data in the section looked at
### Structure
- the sidebar that contains main menu pages, ordered based on importance
- the main container that displays the needed data from the page


### Functionality
- TBD

### Features
- mobile layout/ web layout
- feature for correcting the missing/wrong data, by uploading a correction file
- a section to visualize the kpis in relation to the goals and to obtain the main tables in report, without downloading the report first

## KPI Caluculation
### KPIs
- Gender diversity for paygrades for various markets. Main grades: G34+ and G37+
- Gender distribution in education
- ethnic distribution per markets

### Calculations
- Aggregate the population for a specified region
- Aggregate the population for a speciffic market, depending on the KPI looked at
- Calculate the percentages of the females in the population looked at and retain a list of employees for the same kpi to make it reusable
- Aggregate and calculate ethnic diversity for a certain region
- calculate the goals and ambitions of the region and market based on the type of KPI looked at
- calculate the population present and population movements between two relative dates


## Report design
- section for the raw numbers and percentages of the population targeted in the kpi
- section for population movements (if it's the case)
- Section for comments from the receiver of the report
- Section for corrections
