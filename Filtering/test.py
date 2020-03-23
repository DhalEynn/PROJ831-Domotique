# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:36:21 2020

@author: robin
"""
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import numpy as np
 
def test():
    city=['Delhi','Beijing','Washington','Tokyo','Moscow']
    pos = np.arange(len(city))
    Happiness_Index=[60,40,70,65,85]
    
    plt.bar(pos,Happiness_Index,color='blue',edgecolor='black')
    plt.xticks(pos, city)
    plt.xlabel('City', fontsize=16)
    plt.ylabel('Happiness_Index', fontsize=16)
    plt.title('Barchart - Happiness index across cities',fontsize=20)
    plt.show()
    
import plotly.graph_objects as go 
from plotly.offline import plot
animals=['giraffes', 'orangutans', 'monkeys']

fig = go.Figure([go.Bar(x=animals, y=[20, 14, 23])])
plot(fig)