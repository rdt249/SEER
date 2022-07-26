import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.optimize import curve_fit

# import warnings
# from statsmodels.tools.sm_exceptions import ValueWarning,RuntimeWarning
# warnings.simplefilter('ignore',ValueWarning)
# warnings.simplefilter('ignore',RuntimeWarning)

device_source = 'input/devices.csv'
flux_source = 'GOES 6-hour'

time = pd.Index([])

def bendel(x,A,S):
    y = (np.array(x) - float(A)) * np.sqrt(18 / float(A))
    y[y < 0] = 0
    return float(S) * np.power(1 - np.exp(-0.18 * np.sqrt(y)),4)

def power(x,a,b):
    return float(a) * np.power(np.array(x,float),float(b))

def linear(x,m):
    return float(m) * np.array(x,float)

def get_data():
    if flux_source.split()[0] == 'ACE':
        if flux_source.split()[1] == '2-hour':
            df = pd.read_csv('https://services.swpc.noaa.gov/text/ace-sis.txt',skiprows=16,header=None,delimiter='\s+')
            df['Time'] = df[0].astype(str) + df[1].astype(str) + df[2].astype(str) + df[3].astype(str).str.zfill(4)
            df['Time'] = pd.to_datetime(df['Time'],format='%Y%m%d%H%M')
            df = df.set_index('Time')[[7,9]].astype(float)
            df.columns = [10,30]
            df = df.stack().reset_index().set_index('Time')
            df.index = df.index.strftime('%Y-%m-%d %H:%M')
            df.columns = ['E (MeV)','Flux (pfu)']
            df['Flux (pfu)'] = df['Flux (pfu)'].replace(-100000,np.nan)
    if flux_source.split()[0] == 'GOES':
        url = 'https://services.swpc.noaa.gov/json/goes/primary/integral-protons-'+flux_source.split()[1]+'.json'
        df = pd.read_json(url)
        df['Time'] = pd.to_datetime(df['time_tag'])
        df = df.loc[df['satellite'] == 16]
        df['E (MeV)'] = df['energy'].str.split('=',expand=True)[1].str.split(expand=True)[0].astype(float)
        df = df.set_index('Time').sort_values(by=['Time','E (MeV)'],ascending=True)
        df.index = df.index.strftime('%Y-%m-%d %H:%M')
        df = df.loc[df['E (MeV)'] > 1]
        df['Flux (pfu)'] = df['flux']
        df = df[['E (MeV)','Flux (pfu)']]
    return df.dropna()

def refresh():
    devices = pd.read_csv(device_source)
    devices['Effect'] = devices['Device'].str[:] + ' [' + devices['Effect'].str[:] + ']'
    devices = devices.set_index('Effect')
    devices['FOM (cm2)'] = devices['Saturation'] * np.power(np.log(1000/devices['Threshold']),1.25)

    protons = get_data()
    protons.to_csv('output/protons.csv')

    global time
    time = protons.index.unique()
    effects = devices.index.unique()

    spectra = pd.DataFrame(index=time,columns=['slope','intercept'])
    for t in time:
        row = protons.loc[t]
        spectra.loc[t,:] = np.polyfit(np.log10(row['E (MeV)']),row['Flux (pfu)'],1)
    spectra.to_csv('output/spectra.csv')

    rates = []
    x = np.geomspace(1,1000,1000)
    for t in time:
        spectrum = np.poly1d(spectra.loc[t,:].values)(np.log10(x))
        for effect in effects:
            row = devices.loc[effect]
            device = bendel(x,row['Threshold'],row['Saturation'])
            rate = (spectrum * device).sum()
            rates += [[t,effect,rate,row['FOM (cm2)'],row['Threshold'],row['Saturation']]]
    columns = ['Time','Effect','Rate (/s)','FOM (cm2)','Threshold','Saturation']
    rates = pd.DataFrame(rates,columns=columns).set_index('Time')
    rates.to_csv('output/rates.csv')

    severity = pd.DataFrame(index=time,columns=['S (/cm2/s)','slope','intercept','estimate'])
    for t in time:
        row = rates.loc[t][:]
        opt,cov = curve_fit(linear,row['FOM (cm2)'],row['Rate (/s)'])
        est = 120 * spectra.loc[t]['slope'] + 50.58 * spectra.loc[t]['intercept']
        severity.loc[t][:] = list(opt) + spectra.loc[t][['slope','intercept']].to_list() + [est]
    severity['error'] = severity['S (/cm2/s)'] - severity['estimate']
    severity.to_csv('output/severity.csv')

def plot_protons():
    protons = pd.read_csv('output/protons.csv')
    return px.line(protons,'Time','Flux (pfu)',color='E (MeV)',log_y=True,range_y=[1e-2,1e4])

def plot_spectra(t = None):
    protons = pd.read_csv('output/protons.csv')
    if t == None: protons = protons.loc[protons['Time'] == protons['Time'].min()]
    else: protons = protons.loc[protons['Time'] == t]
    return px.scatter(protons,'E (MeV)','Flux (pfu)',log_x=True,log_y=True,
        trendline='ols',trendline_options={'log_x':True},
        range_y=[0.9 * protons['Flux (pfu)'].min(),1.1 * protons['Flux (pfu)'].max()])

def plot_rates():
    rates = pd.read_csv('output/rates.csv')
    return px.line(rates,'Time','Rate (/s)',color='Effect',log_y=True,range_y=[1e-14,1e-7])

def plot_fom(t=None):
    rates = pd.read_csv('output/rates.csv')
    if t == None: rates = rates.loc[rates['Time'] == rates['Time'].min()]
    else: rates = rates.loc[rates['Time'] == t]
    return px.scatter(rates,'FOM (cm2)','Rate (/s)',log_x=True,log_y=True,
        hover_name='Effect',hover_data=['Threshold','Saturation'],
        trendline='ols',trendline_options={'add_constant':False})

import plotly.graph_objects as go
def plot_plane():
    severity = pd.read_csv('output/severity.csv')
    points = severity[['slope','intercept','S (/cm2/s)']].values
    centroid = points.mean(axis=0)
    u,sigma,v = np.linalg.svd(points - centroid)
    normal = v[2] / np.linalg.norm(v[2])
    print('%ex + %ey + %ez = %e'%(*normal,np.dot(centroid,normal)))
    xx,yy = np.meshgrid(np.linspace(-0.1,0,100),np.linspace(0.25,0.55,100))
    d = normal[0] * centroid[0] + normal[1] * centroid[1] + normal[2] * centroid[2]
    z = (-normal[0] * xx - normal[1] * yy + d) * 1. /normal[2]
    fig = px.scatter_3d(severity,'slope','intercept','S (/cm2/s)')
    fig.add_trace(go.Surface(x=xx,y=yy,z=z))
    return fig

def plot_severity():
    severity = pd.read_csv('output/severity.csv')
    return px.line(severity,'Time','S (/cm2/s)')

def plot_combo(t=None):
    fig = make_subplots(rows=2,cols=1,shared_xaxes=True,vertical_spacing=0.1)
    for trace in plot_protons().select_traces(): fig.add_trace(trace,row=1,col=1)
    for trace in plot_severity().select_traces(): fig.add_trace(trace,row=2,col=1)
    fig.update_yaxes(title_text='Flux (pfu)',type='log',range=[-2,4],row=1,col=1)
    fig.update_yaxes(title_text='S (/cm2/s)',range=[0,50],row=2,col=1)
    fig.update_layout(height=600)
    if t != None: fig.add_vline(t)
    return fig

def report(fig):
    result = px.get_trendline_results(fig)
    return '\n\n\n\n\n' + str(result.px_fit_results.iloc[0].summary())

refresh()
