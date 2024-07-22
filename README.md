# A kpi_reporting Flet app

### This Section is under construction. More will be available soon

<div id="header" align="center">
  <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbHR1N25kZGp6ZWN1ajVoM243eGJ6emNlNnVjOWgycTEycHIyM25rYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/fVeAI9dyD5ssIFyOyM/giphy.gif" width="500"/>
</div>

## Objective
To calculate and extract various KPI Reports from a data source. 

### KPIs calculated
- total number and percentage of women in a given period;
- total number and percentage of women in a given seniority level;
- total number and percentage of genders in a given seniority level;
- percentage of ethnicities in a given area;

## Usage
to install requirements:
```
pip install -r requirements.txt
```
To run the app:

```
flet run [app_file]
```

## Structure
An interface similar with Trello, that contains a sidebar used for navigation, with x number of options, speciffic for the task at hand: the
1. Show Home
2. Reports
3. Show Data
4. Settings

### Show Home
Shows the front page of the app, containing an overview  of all kpis calculated, based on departament
Objects: 
- a departament dropdown: for choosing the departament which data we want to visualize
- the table containing data related to the departament chosen

### Reports
Shows a page from where the user can set the data and quarters for which they need a report

### Show Data
Shows a dashboard with relevant kpi tracking and tools to customize the needed data. 

### Settings
A settings page for admin user or for setting preferences for the app

## Presentation

## Raw Data
The data offered and presented was created using [mockaroo api](https://mockaroo.com/) and has no correlation with real people. This data is esential for the KPI reports supposed above

## How to

