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
        dcc.Input(
        id='input-sentence',
        placeholder='Enter a sentence...',
        type='text',
        value=''
    ),
    html.Br(),
    html.Button('Submit', id='submit-button')
    ],
    style=card_style,
)

prediction_card = dbc.Card(
    [
        html.Br(),
        html.Div(id='output-prediction')
    ],
    style=card_style,
)

title_card = dbc.Card(
    [
        html.H1("Arabic Dialect Prediction-تَحدِّدُ اَللَّهْجَةُ", style={'font-family': 'IBM Plex Sans Arabic', 'font-size':'100px'})
    ],
    style=card_style,
)

app.layout = html.Div([
    html.Div([
        title_card
    ],style={
                'display': 'flex',
                'flex-direction': 'column',
                'align-items': 'center',
                'justify-content': 'center'
                # 'height': '100vh'
            }),
    html.Br(),
    input_card,
    prediction_card
])

@app.callback(
    dash.dependencies.Output('output-prediction', 'children'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('input-sentence', 'value')]
)
def predict(n_clicks, input_sentence):
    # Define the endpoint URL
    url = "http://localhost:8080/predict"

    # Define the request parameters
    params = {
        "sentence": input_sentence,
    }

    # Send a POST request to the endpoint with the parameters
    response = requests.post(url, json=params)

    # Check the response status code
    if response.status_code == 200:
        # The request was successful, so return the prediction
        return str(response.json())
    else:
        # The request failed, so return an error message
        return "Error: {}".format(response.content)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
