# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 21:58:51 2023

@author: axl_a
"""

# import plotly.express as px
import pandas as pd
import ast
import re
import plotly.graph_objects as go
# import kaleido

''' Pre-requisites '''
## Source and read in data
src = "https://github.com/Alex-Caian/Plotly_demo/blob/main/Data/Demo_data_plotly.csv?raw=True"
data = pd.read_csv(src)
## Quick fix for dtype mismatch on arrays
for cols in ['Advantages', 'Disadvantages']:
    data[cols] = data[cols].apply(ast.literal_eval)

## Color mapping for legends
colors_map = {'Balanced - Version 1': 'rgba(239, 130, 117, .6)', 'Balanced - Version 2': 'rgba(239, 130, 117, .6)',
             'Moderately rushed': 'rgba(138, 79, 125, .6)', 'Extreme performance':'rgba(25, 133, 161, .6)',
             'Wildcard plan':'rgba(233, 206, 44, .6)'}

''' Plotly Script '''
fig = go.Figure(
    data = go.Scatterpolar(),
    layout = go.Layout(
        updatemenus=[dict(
        type="buttons",
        buttons=[
        dict(label="Play/Pause", method="animate", visible=True, ## Play button 
            args=[None, {'frame': {'duration': 2250, 'redraw': True}, 'fromcurrent': True}],
            args2=[(), {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}]),
            
        dict(label='[Toggle] Outline', method='update', visible = False, ## Outline toggle
            args = [{'visible':(True, True)}],
            args2 = [{'visible':(True, False)}]),
            
        dict(label='[Toggle] Dark Mode', method='relayout', visible=True, ## Dark Mode
            args = [{'paper_bgcolor':'#192734',
                     'polar.angularaxis.tickfont.color': '#FFFFFF',
                     'polar.radialaxis.color':'#FFFFFF',
                     'legend.font.color':'#FFFFFF',
                     'legend.bgcolor':'rgba(127, 127, 127, .45)'}, [None]],
            args2 = [{'paper_bgcolor':'#FFFFFF', 
                     'polar.angularaxis.tickfont.color': '#001450',
                     'legend.font.color':'#000000',
                      'legend.bgcolor':'rgba(127, 127, 127, .25)',
                     'polar.radialaxis.color':'#000000'}, [None]]),
        dict(label = "RESET", method="animate", visible=True,
            args = [None, {'frame': {'duration':0, 'redraw':False}, 'fromcurrent':False}]) ## Reset button
                ])],
                title = "Showcase of strategic plans",
                title_x = .56,
                title_font = {'size':24, 'color': '#001450', 'family':'Clear-Sans'}),
    frames = [go.Frame(
        data = ({'type':'scatterpolar',
                'r':data.iloc[i,1:8],
                'theta':data.columns[1:8],
                'fill':'toself',
                'fillcolor':colors_map[data.loc[i, 'Description']],
                'line':go.scatterpolar.Line({'color':re.sub(r'\.\d{1}', '1', colors_map[data.loc[i, 'Description']]), 'dash':'solid'}),
                'opacity':1,
                'visible':True,
                'name':'Plan: '+data.loc[i,'Description'],
                'showlegend':True,
                'marker':{'opacity':1, 'symbol':0, 'size':9},
                'mode':'markers+lines',
                'text': "<br>".join([f'Grade {v} in {k}' for k,v in dict(data.iloc[i,1:8]).items()]),
                'texttemplate':'%{hovertext}>',
                'hovertext':[f"Grade {v} in {k}" for k,v in dict(zip(data.columns[1:8], data.iloc[i,1:8])).items()],
                'hovertemplate':'%{hovertext}<extra></extra>',
                }),
        layout = go.Layout(
                    title=f"Strategic plan: <b>{data.iloc[i,0]}</b>",
                    title_x=0.55,
     annotations = [{'bordercolor':'#000000',
                    'bgcolor':'rgba(127, 127, 127, .75)',
                    'x':-.23,
                    'y':0.02,
                    'showarrow':False,
                    'borderwidth':2.5,
                    'xref':'paper',
                    'yref':'paper',
                    'font':{'color':'#FFFFFF', 'family':'Clear-Sans'},
                    'text':'<span style="font-size: 15px;">' + '<br>'.join(['<span style="text-decoration: underline;">Plan Advantages</span>', 
                                       '', '<br>'.join(["• "+ x for x in data.loc[i, "Advantages"]]),
                                       '', '',
                                       '<span style="text-decoration: underline;">Plan Disadvantages</span>',
                                       '', '<br>'.join(["• "+ x for x in data.loc[i, "Disadvantages"]])]) + "</span>"
                    }]
    )) for i in range(len(data))])

fig.update_polars(radialaxis_range=[0, 10])
fig.update_layout(polar={'radialaxis':{'gridcolor': '#FFFFFF', 'color':'#000000',
                                           'tickvals':[0,2,4,6,8,10], 
                                           'ticktext':["Grade  <b>" + str(x) + "</b>" for x in range(0,11,2)]},
                             'angularaxis':{'tickfont':{'size':17, 'color':'#000000', 'family':'Clear-Sans'}},
                             'bgcolor': "rgba(127, 127, 127, .75)"},
    images = [{'source': 'https://i.imgur.com/NGajozI.png',
                              'x':.9,
                              'y':1.12,
                              'xref':'paper',
                              'yref':'paper',
                              'sizex':.40,
                              'sizey':.40,
                              'opacity':1,
                                'layer':'above'}],
    legend = {'x':-.13, 'y':1.15, 'bordercolor':'#000000', 'bgcolor':'rgba(127, 127, 127, .25)',
            'font':{'size':19, 'color':'#000000', 'family':'Clear-Sans'}},
    title_font = {'size':30,'color':'rgba(127, 127, 127, .95)','family':'Clear-Sans'},
    title_x = .55
                     )
fig.show()