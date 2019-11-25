import random
import plotly.graph_objs as go
from plotly.subplots import make_subplots

class Display(object):

    def __init__(self,vocabulary):
      self.vocabulary = vocabulary

    def generateRandomColor(self):
        """ Generates random RGB color """
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        hexCode = self.rgb2hex(r,g,b)
        return hexCode

    def rgb2hex(self,r,g,b):
        """ converts RGB color to hexadecimal """
        return '#%02x%02x%02x' % (r,g,b)
    
    def displayPieChartSummary(self, dictionnary,title):
        """ displays pie chart figure for the given dictionnary """
        specs = []

        for i in range(4):
            table = []
            for j in range(5):
                table.append({'type':'domain'})
            specs.append(table)

        figure = make_subplots(rows=4, cols=5,specs=specs)
        (i,j) = (1,1)

        for partition in self.vocabulary.getPartitions():
            if j == 6:
                j = 1
                i += 1
            labels = []
            values = []
            partitionName = partition.getAttName()
            for modality in partition.modalities:
                key = partitionName + " : " + modality
                labels.append(modality)
                values.append(dictionnary[key])
            figure.add_trace(go.Pie(labels=labels,values=values,title=partitionName,titleposition="middle center"),i,j)
            j += 1

        figure.update_traces(hole=.5, hoverinfo="label+percent")
        figure.update_layout(title_text=title,height=1000)
        figure.show()

    def displayBubbleChart(self, dict, title):
        """ displays bubble chart figure for the given dictionnary """
        values = []
        sizes = []
        labels = []
        colors = []
        for key in dict:
            if dict[key] > 0:
                labels.append(str(key))
                values.append(dict[key])
                randomColor = self.generateRandomColor()
                colors.append(randomColor)
                if dict[key] < 0.1:
                    sizes.append(0.1*100)
                else:
                    sizes.append(dict[key]*100)
        figure = go.Figure(data=[go.Scatter(
            x=labels, y=values,
            mode='markers',
            marker_color=colors,
            marker_size=sizes)
        ])
        figure.update_xaxes(showgrid=False, zeroline=False)
        figure.update_yaxes(showgrid=False, zeroline=False)
        figure.update_layout(title_text=title)
        figure.show()
     
