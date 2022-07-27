import seer, cite
from datetime import datetime
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

app = Dash(title='SEER',external_stylesheets=[dbc.themes.BOOTSTRAP])

sources = [
    'GOES','ACE'
    # 'GOES 6-hour','GOES 1-day','GOES 3-day','GOES 7-day','ACE 2-hour','ACE 1-day'
]

app.layout = dbc.Container([
    dcc.Markdown('###### University of Tennessee at Chattanooga ~ Stephen Lawrence'),
    html.Hr(),
    dcc.Markdown(cite.introduction,mathjax=True),
    html.Hr(),
    dcc.Markdown(cite.description,mathjax=True),
    html.Hr(),
    dbc.Row([
        dbc.Col(dcc.RadioItems(sources,value=seer.flux_source,inline=True,id='source'),width=5),
        dbc.Col(html.Div('Timestamp: ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),id='timestamp'),width=5),
        dbc.Col(html.Button('Refresh Data',id='refresh'),width=2)
    ]),
    dcc.Loading([
        dbc.Row([
            dbc.Col([dcc.Graph(figure=seer.plot_combo(seer.time[0]),id='combo')])
        ]),
    ]),
    dcc.Loading([
        dbc.Row([
            dbc.Col([],width=1),
            dbc.Col([dcc.Slider(0,len(seer.time) - 1,1,value=0,marks=None,id='slider')]),
            dbc.Col([],width=1)
        ]),
    ]),
    dcc.Loading([
        dbc.Row([
            dbc.Col([dcc.Graph(figure=seer.plot_spectra(seer.time[0]),id='spectra')],width=7),
            dbc.Col(html.Pre('',style={'font-size':'8px'},id='spectra_report'),width=5)
        ]),
    ]),
    dcc.Loading([
        dbc.Row([
            dbc.Col([dcc.Graph(figure=seer.plot_fom(seer.time[0]),id='fom')],width=7),
            dbc.Col(html.Pre('',style={'font-size':'8px'},id='fom_report'),width=5)
        ]),
    ]),
    html.Hr(),
    dcc.Markdown(cite.future_work,mathjax=True),
    html.Hr(),
])

@app.callback(
    Output('timestamp','children'),
    Output('slider','max'),
    Input('refresh','n_clicks'),
    Input('source','value'),
    prevent_initial_call = True)
def refresh_data(n,source):
    seer.flux_source = source
    seer.refresh()
    return 'Timestamp: ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),len(seer.time) - 1

@app.callback(
    Output('combo','figure'),
    Output('spectra','figure'),
    Output('spectra_report','children'),
    Output('fom','figure'),
    Output('fom_report','children'),
    Input('slider','value'),
    Input('timestamp','children'),
    prevent_initial_call=False)
def update_figs(t,timestamp):
    combo = seer.plot_combo(seer.time[t])
    spectra = seer.plot_spectra(seer.time[t])
    fom = seer.plot_fom(seer.time[t])
    return combo,spectra,seer.report(spectra),fom,seer.report(fom)

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0',port='8050')