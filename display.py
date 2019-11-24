import plotly.graph_objs as go
from plotly.subplots import make_subplots

class Display(object):
    def __init__(self,vocabulary):
      self.vocabulary = vocabulary

    def displayPieChartSummary(self, dictionnary,title):
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

    def displayLinkedTerms(self,linkedTermsDictionnary,listOfTerms,threshold):
        values = []
        labels = []
        for key in linkedTermsDictionnary:
            if(linkedTermsDictionnary[key] > 0): #if the correlation is > 0, we display it
                labels.append(str(key))
                values.append(linkedTermsDictionnary[key])
        figure = go.Figure(data=[go.Pie(labels=labels,values=values,hole=.5)])
        figure.update_traces(hoverinfo='label+percent', textfont_size=20,marker=dict(line=dict(color='#000000', width=2)))
        figure.update_layout(title_text="Linked terms to "+str(listOfTerms)+" with threshold = "+str(threshold))
        figure.show()

    def displayAtypicalTerms(self, dict, listOfTerms, threshold):
        values = []
        sizes = []
        labels = []
        for key in dict:
            if dict[key] > 0:
                labels.append(str(key))
                values.append(dict[key])
                if dict[key] < 0.1:
                    sizes.append(0.1*100)
                else:
                    sizes.append(dict[key]*100)
        figure = go.Figure(data=[go.Scatter(
            x=labels, y=values,
            mode='markers',
            marker_size=sizes)
        ])
        figure.update_xaxes(showgrid=False, zeroline=False)
        figure.update_yaxes(showgrid=False, zeroline=False)
        figure.update_layout(title_text="Atypical terms in 2008 flights with " + str(listOfTerms) + " with threshold = " + str(threshold))
        figure.show()
