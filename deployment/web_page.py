import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import requests

external_stylesheets = [
    {
        'href': 'https://fonts.googleapis.com/css2?family=Open+Sans&display=swap',
        'rel': 'stylesheet'
    },
    dbc.themes.BOOTSTRAP
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
card_style = {
    # 'width': '300px',
    # 'height': '300px',
    # 'border': '1px solid black',
    'padding': '20px',
    'margin': '20px',
    'display': 'inline-block',
    'vertical-align': 'top'
}
input_card = dbc.Card(
    [
    # dbc.Input(id='input-sentence',
    #         placeholder='Enter a sentence...',
    #         type='text',
    #         value='' ,
    #         size="lg", className="mb-3"),
    dcc.Textarea(id='input-sentence', placeholder='Enter a sentence...', 
                     value='', style={'width': '100%','height':'40%'}),
    html.Br(),
    dbc.Button("Submit", color="secondary", className="me-1", id='submit-button', style={'width': '100%'})
    ],
    style={
        "background-color": "#F4F4F4",
        'width': '50%',
        'padding': '20px',
        'margin': '20px',
        'display': 'inline-block',
        'vertical-align': 'top',
        'border': 'none',
        'box-shadow': '0 0 5px 5px rgba(0, 0, 0, 0.1)'
    }
)


info_card = dbc.Card(
    [
        html.Div(['''This an apllication that detect arabic dialect,
          Enter your arabic dialect end will predict which of these 
          dialects (EG: Egypt, LB: Lebanon, LY: Libya, MA: Morocco, SD: Sudan) it belongs'''],
          style={'font-family': 'IBM Plex Sans Arabic', 'font-size':'28px'}),
    ],
    style={
        "background-color": "#EEEEEE",
        'width': '50%',
        'padding': '20px',
        'margin': '20px',
        'display': 'inline-block',
        'vertical-align': 'top',
        'border': 'none',
        'box-shadow': '0 0 5px 5px rgba(0, 0, 0, 0.1)'
    }
)

prediction_card = dbc.Card(
    [
        html.Div(['Prediction will be returned here'],id='output-prediction',
                 style={'font-family': 'IBM Plex Sans Arabic', 'font-size':'28px'})
        # dcc.Textarea(id='output-prediction', placeholder='Prediction will be displayed here...', 
        #              value='', readOnly=True, style={'width': '100%'})
    ],
    style={
        "background-color": "#F4F4F4",
        'width': '50%',
        'padding': '20px',
        'margin': '20px',
        'display': 'inline-block',
        'vertical-align': 'top',
        'border': 'none',
        'box-shadow': '0 0 5px 5px rgba(0, 0, 0, 0.1)'
    }
)

title_card = dbc.Card(
    [
        html.H1("Arabic Dialect Prediction-تَحدِّدُ اَللَّهْجَةُ", 
            style={'font-family': 'IBM Plex Sans Arabic', 'font-size':'100px', 'margin-top':'1%'})
    ],
    style={
        "background-color": "#EEEEEE",
        'padding': '20px',
        'margin': '20px',
        'display': 'inline-block',
        'vertical-align': 'top',
        'border': 'none',
        'box-shadow': '5px 5px 5px rgba(0, 0, 0, 0.1)'
    }
)

app.layout = html.Div([
    html.Div([
        title_card,
        info_card
    ],style={
                'display': 'flex',
                'flex-direction': 'column',
                'align-items': 'center',
                'justify-content': 'center'
                # 'height': '100vh'
            }),
    html.Br(),
    dbc.Col([input_card, prediction_card], style={'display': 'flex',
                'flex-direction': 'column',
                'align-items': 'center',
                'justify-content': 'center'})
],style={
        "background-color": "#F4F4F4",
        "height": "100vh",
        "width": "100vw",
    },)

@app.callback(
    dash.dependencies.Output('output-prediction', 'children'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('input-sentence', 'value')]
)
def predict(n_clicks, input_sentence):
    # Define the endpoint URL
    url = "http://localhost:8080/predict"

    if not input_sentence:
        return 'Prediction will be returned here'

    # Define the request parameters
    params = {
        "sentence": input_sentence,
    }

    # Send a POST request to the endpoint with the parameters
    response = requests.post(url, json=params)

    # Check the response status code
    if response.status_code == 200:
        # The request was successful, so return the prediction
        return response.json()['sentence']
    else:
        # The request failed, so return an error message
        return "Error: {}".format(response.content)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
