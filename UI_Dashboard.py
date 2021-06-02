import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import webbrowser
import plotly.graph_objects as go

project_name = "Human Sentiments Analysis Using AI Based Techniques"
app = Dash(update_title='Loading...', external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions = True)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')
    
def load_model():
    global vocab
    global pickle_model
    global df
    global dfs
    df = pd.read_csv('balanced_reviews.csv')
    dfs = pd.read_csv('scrappedReviews.csv')
    with open("pickle_model.pkl", 'rb') as file:
        pickle_model = pickle.load(file)
    with open("vocab_model.pkl", 'rb') as voc:
        vocab = pickle.load(voc)
        
def check_review(reviewText):
     global vectorized_review
     global transformer
     global revviewText
     transformer = TfidfTransformer()
     loaded_vec = CountVectorizer(decode_error ='replace',vocabulary = vocab)
     reviewText = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))
     return pickle_model.predict(reviewText)
     
def create_app_ui():
    global reviews
    global dfs
    global df
    df = df.dropna()
    df['Positivity'] = np.where(df['overall']>3, 1, 0)
    global labels
    labels = ['Positive Reviews', 'Negative Reviews', 'Neutral Reviews']
    values = [df[df['overall']> 3].dropna().shape[0], df[df['overall'] < 3].dropna().shape[0], df[df['overall']==3].dropna().shape[0]]
    colors = ['#00cd00', '#d80000', '#a6a6a6']
    
    labels1 = ['+ve Reviews', '-ve Reviews']
    values1 = [len(df[df['Positivity']==1]), len(df[df['Positivity']==0])]
    
    main_layout = dbc.Container(
        dbc.Jumbotron(
            [
                html.H1(id = 'Main_title', children = project_name,
                           className='display-3 mb-4',
                           style={'font': 'sans-seriff', 'font-weight': 'bold', 'font-size': '50px', 'color': 'black'}),
                html.Hr(),
                html.H4(id = 'heading', children = 'Pie Chart Visualisation of Reviews',
                        className='display-3 mb-4',
                        style={'font': 'sans-seriff', 'font-weight': 'bold', 'font-size': '30px', 'color': 'blue'}),
                dbc.Container([
                    dcc.Graph(
                        figure={'data': [go.Pie(labels=labels, values=values, pull =[0.2,0,0], textinfo='value', marker=dict(colors=colors, line=dict(color='#000000', width=2)))],
                                'layout': go.Layout(height=500, width=900, autosize=False)},
                        style = {'margin-top': '30px', 'margin-bottom': '30px'},
                        className='d-flex justify-content-center'
                        ),
                    ]),
                html.Hr(),
                html.P(id='heading4', children='Positive-Negative Distribution...',
                           className='display-3 mb-4', style={'font': 'sans-seriff', 'font-weight': 'bold', 'font-size': '30px', 'color': 'blue'}),
                    
                dbc.Container(
                    dcc.Graph(id='example-graph',
                              figure={'data': [go.Bar(y=labels1, x=values1, orientation='h', marker=dict(color="MediumPurple"))],
                                     'layout': go.Layout(xaxis={'title': 'Sentiments'}, yaxis={'title': 'Emotions'}),
                                }
                            )
                    ),
                html.Hr(),
                html.H5(id = 'heading2', children = 'Write, what you feel!!',className='display-3 mb-4',style={'font': 'sans-seriff', 'font-weight': 'bold', 'font-size': '30px', 'color': 'black'}),         
                dcc.Textarea(id = 'textarea',className = "mb-3",placeholder = 'Enter your review here.....',style = {'width':'100%', 'height':100}),
                dbc.Button("You can check- ", color="dark", className="mt-2 mb-3", id = 'button', style = {'width': '300px',}),
                html.Div(id = 'result'),
                html.Hr(),
                html.P(id = 'heading1', children = "Scrapped Etsy Review Sentiments...",
                       className='display-3 mb-4', style={'font': 'sans-serif', 'font-weight': 'bold', 'font-size': '30px', 'color': 'black'}),
                dbc.Container([
                    dcc.Dropdown(id = 'dropdown', 
                                 placeholder = "SELECT A REVIEW :- ",
                                 options=[{'label': i[:100] + "...", 'value': i} for i in dfs.reviews],
                                 value = dfs.reviews[0],
                                 style={'margin':'10px'}
                                 )
                    ]),
                html.Div(id = 'result1'),
               ],
                className='text-center'
            ),
            className='mt-4'
    )    
    return main_layout    


@app.callback(
    Output('result','children'),
    [
    Input('button','n_clicks')
    ],
    State('textarea', 'value')
    )
def update_app_ui(n_clicks, textarea):
    print("Data Type : ", str(type(n_clicks)))
    print("Value : ", str(n_clicks))
    print("Data Type : ", str(type(textarea)))
    print("Value : ", str(textarea))
    response = check_review(textarea)
    if(response[0]==0):
        return dbc.Alert("Ahh! Negative Feedback..", color="danger")
    elif(response[0]==1):
        return dbc.Alert("Ahhaa! This is a positive feedback..", color="success")
    else:
        return dbc.Alert("No review yet", color="dark")


@app.callback(
    Output('result1','children'),
    [
    Input('dropdown','value')
    ]
    )
def update_dropdown(value):
    response = check_review(value)
    if(response[0]==0):
        return dbc.Alert("Ahh! Negative Feedback..", color="danger")
    elif(response[0]==1):
        return dbc.Alert("Ahhaa! This is a positive feedback..", color="success")
    else:
        return dbc.Alert("No review yet", color="dark")
    
def main():
    global df
    global project_name
    global app
    print("Start of my Project")
    open_browser()
    load_model()
    
    app.title = project_name
    app.layout = create_app_ui() #container object to make a blank page
    app.run_server(debug = False)
    print("End of my Project")
    
    project_name = None
    app = None

# 5. caling the main function
if __name__ == '__main__':
    main()