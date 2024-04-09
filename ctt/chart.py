from .static.lib.pychartjs.pychartjs import BaseChart, ChartType
from .static.lib.pychartjs import Color


class ChartJs():
    
    def linear_gradient(ctx, color1, color2):
        color = Color.JSLinearGradient(ctx, 0, 0, 1000, 0,
                                        (0, color1), 
                                        (1, color2)
                                        ).returnGradient()
        return color

    
    class LineGraph(BaseChart):

        type = ChartType.Line

        class data:
            data = []
            label = ''
            borderColor =  Color.Purple
            borderWidth = 3
            fill = True
            pointRadius = 0
            tension = 0.1
            # backgroundColor = False

        class labels:
            grouped = []
        
        class options:
            scales = {
                'y': {
                    'beginAtZero': True,
                },
                'x': {
                    'ticks': {
                        'maxTicksLimit': 5
                    }
                },
            }
    

    class BarGraph(BaseChart):

        type = ChartType.Bar

        class data:
            data = []
            label = ''
            backgroundColor =  Color.Purple
            fill = True

        class labels:
            grouped = []
        
        class options:
            scales = {
                'y': {
                    'beginAtZero': True,
                },
                'x': {
                    'ticks': {
                        'maxTicksLimit': 5
                    },
                    
                },
            }

    class DonutChart(BaseChart):

        type = ChartType.Doughnut

        class data:
            data = []
            label = ''
            backgroundColor =  Color.Purple
            fill = True

        class labels:
            grouped = []
        
        class options:
            pass

    class RadarChart(BaseChart):

        type = ChartType.Radar

        class data:
            data = []
            label = ''
            backgroundColor =  Color.Purple
            fill = True

        class labels:
            grouped = []
        
        class options:
            pass

        class pluginOptions:
            legend = {
                'display': False
            }

    class PolarAreaChart(BaseChart):

        type = ChartType.PolarArea

        class data:
            data = []
            label = ''
            backgroundColor =  Color.Purple
            fill = True

        class labels:
            grouped = []
        
        class options:
            scales = {
                'r': {
                    'pointLabels': {
                    'display': True,
                    'centerPointLabels': True,
                    'font': {
                        'size': 12
                        }
                    },
                }
            }

        class pluginOptions:
            legend = {
                'display': False
            }
              
