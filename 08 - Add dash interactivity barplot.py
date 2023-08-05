import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})


# Create a dash application layout
 # Give the title to the dashboard to “Total number of flights to the destination state split by reporting air” using HTML H1 component and font-size as 50.
# Input component Make changes to a component called dcc.Input in a tool called Dash. We are updating its id to be input-year, which is a unique identifier for this specific input field. The default value for this input field will be set to 2010, and the type of input will be a number.
# To make the text larger and more readable, use the style parameter and assign the height of the input box to 50px and font-size to be 35. Use style parameter again and assign font-size of 40 for the whole division
# Output componentAdd dcc.Graph() component to the second division. Update dcc.Graph component id as bar-plot.
app = dash.Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add a html.Div and core input text component
# Finally, add graph component.
app.layout = html.Div(children=[html.H1('Total number of flights to the destination state split by reporting air',
style={'textAlign': 'center', 'color': '#503D36', 'font-size': 50}),
                                html.Div(["Input Year: ", dcc.Input(id='input-year', value='2010', 
                                type='number', style={'height':'50px', 'font-size': 35}),], 
                                style={'font-size': 40}),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id='bar-plot')),
                                ])


# add callback decorator
@app.callback( Output(component_id='bar-plot', component_property='figure'),
               Input(component_id='input-year', component_property='value'))

# Add computation to callback function and return graph
def get_graph(entered_year):
    # Select data based on the entered year
    df =  airline_data[airline_data['Year']==int(entered_year)]
    

    # Group the data by destination state and reporting airline. Compute the total number of flights in each 
    # combination
    # Use plotly express bar chart function px.bar. Provide input data, x and y axis variables, and a chart 
    # title. This will give the total number of flights to the destination state
    bar_data = df.groupby('DestState')['Flights'].sum().reset_index()

    fig = px.bar(bar_data, x= "DestState", y= "Flights", 
    title='Total number of flights to the destination state split by reporting airline') 

    fig.update_layout(title='Flights to Destination State', 
    xaxis_title='DestState', yaxis_title='Flights')

    return fig


    # Group the data by Month and compute the average over-arrival delay time.
    # bar_data = df.groupby('DestState')['Flights'].sum().reset_index()
    # fig = px.bar(bar_data, x= "DestState", y= "Flights", 
    # title='Total number of flights to the destination state split by reporting airline') 

    # fig.update_layout(title='Total number of flights to the destination state split by reporting airline', 
    # xaxis_title='States', yaxis_title='Fights')

    # return fig

    
# Run the app
if __name__ == '__main__':
    app.run_server()