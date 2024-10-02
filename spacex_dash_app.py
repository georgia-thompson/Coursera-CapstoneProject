# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

Launch_Sites =spacex_df["Launch Site"].unique().tolist()
l_launchsites = []
d_temp = {
    "label": "All Sites",
    "value": "ALL"
}
l_launchsites.append(d_temp)
for site in Launch_Sites:
    d_temp = {
        "label": site,
        "value": site
    }
    l_launchsites.append(d_temp)

def AddNames(bSuccess):
    if(bSuccess==1):
        return "Success"
    else:
        return "Failed"

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=l_launchsites, value="ALL", placeholder="Select a Launch Site", searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id="success-pie-chart", component_property="figure"), 
Input(component_id="site-dropdown", component_property="value"))
def get_pie_chart(selelcted_site):
    if(selelcted_site == "ALL"):
        t = "Success Rates for All Launch Sites"
        fig = px.pie(spacex_df, values='class', names='Launch Site',title=t)
        return fig
    else:
        filtered_data = spacex_df[spacex_df["Launch Site"] == selelcted_site]
        filtered_data["name"] = filtered_data["class"].apply(AddNames)
        use_df = filtered_data.groupby("class")["name"].value_counts().reset_index()
        t = "Total Success Launches for Site " + selelcted_site
        fig = px.pie(use_df, values="count", names="name", color="name", title = t, color_discrete_map={"Success":"green", "Failed":"red"})
        return fig
    


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id="success-payload-scatter-chart", component_property="figure"), 
[Input(component_id="site-dropdown", component_property="value"), Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(selected_site, payload_range):
    df = spacex_df
    t = "Correlation Between Payload and Succes for "
    if(selected_site == "ALL"):
        t = t + "All Sites"
    else:
        df = spacex_df[spacex_df["Launch Site"]==selected_site]
        t = t + selected_site
    t = t + " Between " + str(payload_range[0]) + " and "  + str(payload_range[1]) + " KG"
    df = df[df["Payload Mass (kg)"].between(payload_range[0], payload_range[1])]
    fig = px.scatter(df, x="Payload Mass (kg)", y="class", color= "Booster Version Category", title=t)
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
