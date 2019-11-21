import plotly.io as pio
import plotly.graph_objs as go
from plotly.subplots import make_subplots

class Display(object):
    def __init__(self,dictionnary,filteredDictionnary,correlationsDictionnary,atypicalDictionnary):
        self.dictionnary = dictionnary
        self.filteredDictionnary = filteredDictionnary
        self.correlationsDictionnary = correlationsDictionnary
        self.atypicalDictionnary = atypicalDictionnary

    def displaySummary(self):
        subject = []
        values = []
        text = []
        for key in self.dictionnary.keys():
            subject.append(str(key).split(":")[0])
            text.append(str(key).split(":")[1])
            values.append(self.dictionnary[key])
        data = [dict(
            type="scatter",
            textposition="top center",
            text=text,
            x=subject,
            y=values,
            mode='markers+text',
            transforms=[dict(
            type='groupby',
            groups=subject,
            )]
        )]
        fig_dict = dict(data=data)
        pio.show(fig_dict, validate=False)

    def displayCPieChartSummary(self,vocabulary):
        specs = []

        for i in range(4):
            table = []
            for j in range(5):
                table.append({'type':'domain'})
            specs.append(table)

        figure = make_subplots(rows=4, cols=5,specs=specs)
        (i,j) = (1,1)

        for partition in vocabulary.getPartitions():
            if j == 6:
                j = 1
                i += 1
            labels = []
            values = []
            partitionName = partition.getAttName()
            for modality in partition.modalities:
                key = partitionName + " : " + modality
                labels.append(modality)
                values.append(self.dictionnary[key])
            figure.add_trace(go.Pie(labels=labels,values=values,title=partitionName,titleposition="middle center"),i,j)
            j += 1

        figure.update_traces(hole=.5, hoverinfo="label+percent")
        figure.update_layout(title_text="General Summary for 2008 flights in the USA",height=1000)
        figure.show()



