# ========== DASH / PLOTLY / CORE IMPORTS ==========
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash_leaflet import Map, TileLayer, Marker, Tooltip, Popup, CircleMarker
from dash import callback_context

import plotly.express as px
import pandas as pd
import base64
import dash
import logging
import os

from animal_shelter import AnimalShelter

# ========== LOGGING FOR TERMINAL DEBUGGING ==========
logging.basicConfig(level=logging.INFO)
print("RUNNING FILE:", os.path.abspath(__file__))

# ========== DATABASE CONNECTION ==========
username = "briannahrhea"
password = "SNHUCS499Mongo1!"
shelter = AnimalShelter(username, password)

# Load entire collection from MongoDB as initial dataset
df = pd.DataFrame.from_records(shelter.read({}))
if '_id' in df.columns:
    # Drop MongoDB internal ID
    df.drop(columns=['_id'], inplace=True)  

# Logo for header image
image_filename = 'Grazioso_Salvare_Logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# ========== INITIALIZE DASH ==========
app = Dash(__name__)
server = app.server

# ========== DASH LAYOUT ==========
app.layout = html.Div([
    html.H1("Grazioso Salvare Dashboard", style={'textAlign': 'center'}),
    html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), height=200)),
    html.Hr(),

    # --- ANIMAL MATCHER SECTION ---
    # Includes filter by breed, sex upon outcome, and outcome type
    html.Div([
        html.H3("Animal Matcher"),

        html.Label("Filter by Breed"),
        dcc.Dropdown(
            id='breed-filter',
            options=[{'label': b, 'value': b} for b in sorted(df['breed'].dropna().unique())],
            multi=True,
            style={"width": "300px"}
        ),
        html.Br(),

        html.Label("Sex Upon Outcome"),
        dcc.Dropdown(
            id='match-gender',
            options=[{'label': x, 'value': x} for x in df['sex_upon_outcome'].dropna().unique()],
            placeholder="Select Gender", style={"width": "200px"}
        ),
        html.Br(),

        html.Label("Outcome Type"),
        dcc.Dropdown(
            id='match-outcome',
            options=[{'label': x, 'value': x} for x in df['outcome_type'].dropna().unique()],
            placeholder="Select Outcome Type", style={"width": "200px"}
        ),
        html.Br(),

        html.Button("Find Matches", id="match-btn", n_clicks=0),
        html.Div(id="match-results")
    ]),

    html.Hr(),

    # --- FILTER FOR SPECIALIZED RESCUE ANIMALS ---
    # Includes 4 radio buttons (reset, water rescue, mountain/wilderness rescue, and disaster/tracking)
    html.Div([
        html.Label("Rescue Type"),
        dcc.RadioItems(
            id='filter-type',
            options=[
                {'label': 'Reset', 'value': 'RESET'},
                {'label': 'Water Rescue', 'value': 'WATER'},
                {'label': 'Mountain or Wilderness Rescue', 'value': 'MOUNTAIN OR WILDERNESS RESCUE'},
                {'label': 'Disaster or Individual Tracking', 'value': 'DISASTER OR INDIVIDUAL TRACKING'}
            ],
            inline=True
        )
    ]),

    html.Hr(),

    # --- MAIN DATA TABLE ---
    # Displays aac_shelter_outcomes.csv data into organized table
    dash_table.DataTable(
        id='datatable-id',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        row_selectable="multi",
        page_action="native",
        page_current=0,
        page_size=10,
    ),

    # New clickable buttons in table that will be used for bookmark section
    html.Br(),
    html.Button("Bookmark Selected", id="bookmark-btn", n_clicks=0),
    html.Div(id="bookmark-confirmation"),

    html.Hr(),

    # --- BOOKMARK SECTION ---
    # Ability to add, refresh, and clear saved bookmarks
    html.H3("Bookmarked Animals"),
    html.Button("Refresh Bookmarks", id="refresh-bookmarks", n_clicks=0),
    html.Button("Clear All Bookmarks", id="clear-bookmarks", n_clicks=0, style={"marginLeft": "10px"}),
    html.Div(id="bookmark-list"),

    html.Hr(),

    # --- TREND ANALYSIS ---
    # Replaces old pie chart with easier to read line graph with two filter options (outcome type, breed)
    html.Div([
        html.H3("Trend Analysis"),
        dcc.Dropdown(
            id='trend-dropdown',
            options=[{'label': 'Outcome Type', 'value': 'outcome_type'},
                     {'label': 'Breed', 'value': 'breed'}],
            value='outcome_type'
        ),
        dcc.Graph(id='trend-graph')
    ]),

    html.Hr(),

    # --- MAP VISUALIZATION ---
    # Map layout at bottom of page
    html.Div(id='map-id')
], 

style={'padding': '20px'})

# ========== CALLBACKS ==========

# --- TABLE UPDATES ---
@app.callback(
    Output('datatable-id', 'data'),
    [Input('filter-type', 'value'),
     Input('breed-filter', 'value')]
)
def update_table(filter_type, breed_filter):
    query = {}


    # --- RADIO BUTTONS ---
    # Predefined filters for specialized rescue radio buttons
    # Used $regex and $options :i operators to return case insensitive matches
    if filter_type == 'WATER':
        query = {
            "animal_type": "Dog",
            "sex_upon_outcome": "Intact Female",
            "outcome_type": {"$nin": ["Euthanasia"]},
            "$or": [
                {"breed": {"$regex": "Labrador Retriever Mix", "$options": "i"}},
                {"breed": {"$regex": "Pit Bull Mix", "$options": "i"}},
                {"breed": {"$regex": "Beagle Mix", "$options": "i"}}
            ]
        }
    elif filter_type == 'MOUNTAIN OR WILDERNESS RESCUE':
        query = {
            "animal_type": "Dog",
            "sex_upon_outcome": "Intact Male",
            "outcome_type": {"$nin": ["Euthanasia"]},
            "$or": [
                {"breed": {"$regex": "German Shepherd", "$options": "i"}},
                {"breed": {"$regex": "Alaskan Malamute", "$options": "i"}},
                {"breed": {"$regex": "Old English Sheepdog", "$options": "i"}},
                {"breed": {"$regex": "Siberian Husky", "$options": "i"}},
                {"breed": {"$regex": "Rottweiler", "$options": "i"}}
            ]
        }
    elif filter_type == 'DISASTER OR INDIVIDUAL TRACKING':
        query = {
            "animal_type": "Dog",
            "sex_upon_outcome": "Intact Male",
            "outcome_type": {"$nin": ["Euthanasia"]},
            "$or": [
                {"breed": {"$regex": "Doberman Pinscher", "$options": "i"}},
                {"breed": {"$regex": "German Shepherd", "$options": "i"}},
                {"breed": {"$regex": "Golden Retriever", "$options": "i"}},
                {"breed": {"$regex": "Bloodhound", "$options": "i"}},
                {"breed": {"$regex": "Rottweiler", "$options": "i"}}
            ]
        }

    # Logging for additional debugging, had issues previously with table not returning data
    logging.info(f"QUERY USED: {query}")
    records = shelter.read(query if query else {})
    logging.info(f"MATCHING RECORDS: {len(records)}")

    df_result = pd.DataFrame.from_records(records)
    if '_id' in df_result.columns:
        df_result.drop(columns=['_id'], inplace=True)
    # Returning results as list of dictionaries 
    return df_result.to_dict('records')


# --- MATCH ANIMAL CALLBACK ---
# Returns list of animals and ID upon match animal search results
@app.callback(
    Output("match-results", "children"),
    Input("match-btn", "n_clicks"),
    State("breed-filter", "value"),
    State("match-gender", "value"),
    State("match-outcome", "value")
)
# Filter options 
def match_animals(n_clicks, breed_list, gender, outcome):
    if n_clicks > 0:
        query = {}
        if breed_list:
            query['breed'] = {"$in": breed_list}
        if gender:
            query['sex_upon_outcome'] = gender
        if outcome:
            query['outcome_type'] = outcome

        matches = shelter.read(query)

        if not matches:
            return "No animals matched the criteria."

        return html.Ul([
            html.Li(f"{m.get('animal_id', 'N/A')} - {m.get('breed', 'Unknown')} - "
                    f"Sex: {m.get('sex_upon_outcome', 'N/A')} - "
                    f"Outcome: {m.get('outcome_type', 'N/A')}")
            for m in matches
        ])
    return ""


# --- BOOKMARK SECTION ---
# Bookmark animal breed and ID from table selection
@app.callback(
    Output('bookmark-confirmation', 'children'),
    Input('bookmark-btn', 'n_clicks'),
    State('datatable-id', 'data'),
    State('datatable-id', 'selected_rows'),
    prevent_initial_call=True
)
def bookmark_animals(n_clicks, table_data, selected_rows):
    if n_clicks and table_data and selected_rows:
        messages = []
        for idx in selected_rows:
            selected_animal = table_data[idx]
            animal_id = selected_animal.get('animal_id')
            if animal_id:
                animal_id = str(animal_id)
                shelter.save_bookmark(animal_id)
        return html.Ul([html.Li(msg) for msg in messages])
    return "No animals selected to bookmark."


# --- BOOKMARK HANDLING (refresh, remove, clear) ---
# Option to refresh, remove, or clear all saved bookmarks
@app.callback(
    Output('bookmark-list', 'children'),
    Input('refresh-bookmarks', 'n_clicks'),
    Input('clear-bookmarks', 'n_clicks'),
    Input({'type': 'remove-bookmark', 'index': ALL}, 'n_clicks'),
    State({'type': 'remove-bookmark', 'index': ALL}, 'id'),
    prevent_initial_call=True
)
def update_bookmark_list(refresh_clicks, clear_clicks, remove_clicks, remove_ids):
    triggered = callback_context.triggered_id

    if triggered == 'clear-bookmarks':
        shelter.clear_all_bookmarks()
        return "All bookmarks cleared."

    elif isinstance(triggered, dict) and triggered.get('type') == 'remove-bookmark':
        for i, count in enumerate(remove_clicks):
            if count > 0:
                shelter.remove_bookmark(remove_ids[i]['index'])
        return render_bookmarks()

    elif triggered == 'refresh-bookmarks':
        return render_bookmarks()

    return dash.no_update


# --- RENDERING BOOKMARK LIST ---
# Upon bookmark refresh:
def render_bookmarks():
    bookmarks = shelter.get_bookmarks()
    if not bookmarks:
        return "No animals bookmarked."

    return html.Ul([
        html.Li([
            f"{animal['animal_id']} - {animal.get('breed', 'Unknown')}",
            html.Button("Remove", id={'type': 'remove-bookmark', 'index': str(animal['animal_id'])}, n_clicks=0, style={'marginLeft': '10px'})
        ]) for animal in bookmarks
    ])


# --- TREND ANALYSIS GRAPH SECTION ---

    # Resources used to learn this: 
    # https://plotly.com/python/line-charts/
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html

# Trend analysis line graph replacing previous pie chart
@app.callback(
    Output('trend-graph', 'figure'),
    Input('trend-dropdown', 'value')
)
def trend_chart(feature):
    # Read all records from data source using shelter.read() method
    df_trend = pd.DataFrame.from_records(shelter.read({}))
    if '_id' in df_trend.columns:
        df_trend.drop(columns=['_id'], inplace=True)

    # Convert the date_of_birth column to datetime format
    df_trend['date'] = pd.to_datetime(df_trend['date_of_birth'], errors='coerce')
    # If all dates are invalid or missing - return a placeholder empty graph
    if df_trend['date'].isnull().all():
        return px.line(title="No date data available.")

    # Grouping data based on month and feature
    grouped = df_trend.groupby([df_trend['date'].dt.to_period("M").astype(str), feature]).size().reset_index(name='count')

    # Return chart
    return px.line(grouped, x='date', y='count', color=feature, title=f"{feature} Trend")


# --- MAP VISUALIZATION ---

# Resources used to learn this: 
# https://python-visualization.github.io/folium/latest/getting_started.html
# https://www.dash-leaflet.com/
# https://plotly.com/python/density-heatmaps/

@app.callback(
    Output('map-id', 'children'),
    [Input('datatable-id', 'data'),
     Input('datatable-id', 'selected_rows')]
)
def update_map(viewData, selected_rows):
    if not viewData:
        return html.Div("No data to show.")

    # Converting data from table into Pandas DataFrame
    df = pd.DataFrame(viewData)
    # Avoiding map errors by removing rows where latitude or longitude do not exist
    df = df.dropna(subset=['location_lat', 'location_long'])

    # Heat data points
    heat_data = [[row['location_lat'], row['location_long'], 1] for _, row in df.iterrows()]

    markers = [
        CircleMarker(center=[lat, lon], radius=4, color="blue", fill=True)
        for lat, lon, _ in heat_data
    ]

    popup_marker = []

    # When row selected in table, marker will show on map
    if selected_rows and selected_rows[0] < len(df):
        selected = df.iloc[selected_rows[0]]

        # Marker shows on map where location of animal is - displaying breed and name
        popup_marker = [
            Marker(position=[selected['location_lat'], selected['location_long']],
                   children=[
                       Tooltip(selected.get('breed', 'Unknown')),
                       Popup([html.P(f"Name: {selected.get('name', 'N/A')}")])
                   ])
        ]

    # Return map 
    return Map(
        center=[30.2672, -97.7431], 
        zoom=10,
        children=[TileLayer(), *markers, *popup_marker],
        style={'width': '100%', 'height': '600px', 'margin': 'auto', 'display': 'block'}
    )

# ========= RUN ==========
if __name__ == "__main__":
    app.run(debug=True)

