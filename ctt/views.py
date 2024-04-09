import random
from itertools import groupby
from operator import attrgetter, itemgetter
from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Sum, Avg, Max
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import F, ExpressionWrapper, fields
from django.db.models.functions import Coalesce, Greatest
from django.views.decorators.csrf import csrf_exempt



from .forms import TacticForm, GameForm, SessionForm, TacticAttemptForm
from .models import Tactic, Game, Session

from .chart import ChartJs
from .static.lib.pychartjs import Color

def convert_minutes_to_hours(minutes):
    return round(minutes / 60, 2)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfull')
            return redirect('home') 
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')

@login_required
def home_view(request):
    return render(request, 'home.html')
    
@login_required
def training_view(request):

    if request.method == 'POST':
        form = TacticAttemptForm(request.POST)
        if form.is_valid():
            tactic_attempt = form.save(commit=False)
            tactic_attempt.save()

            tactic_attempt.tactic.recompute_duration()

            return JsonResponse({'success': True})
        
    form = TacticAttemptForm()
        
    tactics = Tactic.objects.all()
    games = Game.objects.all()
    sessions = Session.objects.all()

    # Combinar todos los entrenamientos en una lista
    all_training = list(tactics) + list(games) + list(sessions)

    # Agrupar los entrenamientos por fecha
    all_training.sort(key=attrgetter('date'), reverse=True)
    grouped_training = {date: {'trainings': list(group)} for date, group in groupby(all_training, key=attrgetter('date'))}
     # Calcular la duración total para cada fecha
    for date, training_list in grouped_training.items():
        total_duration = sum(training.duration for training in training_list['trainings'])
        grouped_training[date]['total_duration'] = round(total_duration / 60, 1)


    # Renderizar la plantilla con los datos
    return render(request, 'training.html', {
        'tactics': tactics,
        'games': games,
        'sessions': sessions,
        'grouped_training': grouped_training,
        'form': form,
    })


@login_required
def stats_view(request):

    def get_colors(num_colors):
        palette = [
            "#E6194B80",  # Red
            "#F5823180",  # Orange
            "#FFE11980",  # Yellow
            "#BFEF4580",  # Lime
            "#3CB44B80",  # Green
            "#42D4F480",  # Cyan
            "#4363D880",  # Blue
            "#911EB480",  # Purple
            "#F032E680",  # Magenta
            "#46999080",  # Teal
            "#FABEBE80",  # Pink
            "#AAFFC380",  # Mint
            "#E6BEFF80",  # Lavender
            "#9A632480",  # Brown
            "#FFFAC880",  # Beige
            "#80800080",  # Olive
            "#FFD8B180",  # Apricot
            "#00007580",  # Navy
            "#A9A9A980",  # Gray
        ]

        return random.sample(palette, num_colors)

    # def elo():
    #     blitz_data = Game.objects.filter(rithm='Blitz', plataform='Chess.com').values('date').annotate(avg_elo=Avg('elo'))
    #     rapid_data = Game.objects.filter(rithm='Rapid', plataform='Chess.com').values('date').annotate(avg_elo=Avg('elo'))

    #     # Obtener todas las fechas únicas de ambas series
    #     all_dates = set(entry['date'] for entry in blitz_data) | set(entry['date'] for entry in rapid_data)

    #     # Crear diccionarios para mapear fechas a valores de elo
    #     blitz_elo_values = {entry['date']: entry['avg_elo'] for entry in blitz_data}
    #     rapid_elo_values = {entry['date']: entry['avg_elo'] for entry in rapid_data}

    #     # Rellenar los valores de elo para las fechas que faltan
    #     all_blitz_elo_values = [blitz_elo_values.get(date, None) for date in all_dates]
    #     all_rapid_elo_values = [rapid_elo_values.get(date, None) for date in all_dates]

    #     labels = [date.strftime('%Y-%m-%d') for date in all_dates]

    #     bnr_chart = ChartJs.LineGraph()
    #     bnr_chart.labels.grouped = labels
        
    #     # Declarar Apples y Oranges como clases
    #     class Blitz(ChartJs.LineGraph.data):
    #         data = all_blitz_elo_values
    #         label = 'Elo Blitz'

    #     class Rapid(ChartJs.LineGraph.data):
    #         data = all_rapid_elo_values
    #         label = 'Elo Rapid'

    #     # Asignar Apples y Oranges al atributo data
    #     bnr_chart.data.Blitz = Blitz
    #     bnr_chart.data.Rapid = Rapid
    #     bnr_chart.options.scales['x']['ticks']['maxTicksLimit'] = 3

    #     elo = bnr_chart.get()
    #     return elo

    def rapid_elo():
        data = Game.objects.filter(rithm='Rapid', plataform='Chess.com').values('date').annotate(avg_elo=Avg('elo'))

        labels = [entry['date'].strftime('%Y-%m-%d') for entry in data]
        elo_values = [entry['avg_elo'] for entry in data]

        class reChart(ChartJs.LineGraph):
            pass

        reChart = ChartJs.LineGraph()
        reChart.labels.grouped = labels
        reChart.data.data = elo_values
        reChart.data.label = 'Elo Rapid'
        colors = get_colors(2)
        reChart.data.borderColor = ChartJs.linear_gradient('RapidEloCtx', colors[0], colors[1])
        reChart.options.scales['x']['ticks']['maxTicksLimit'] = 3
        reChart.options.scales['y']['beginAtZero'] = False

        rapidElo = reChart.get()
        return rapidElo
    
    def blitz_elo():
        data = Game.objects.filter(rithm='Blitz', plataform='Chess.com').values('date').annotate(avg_elo=Avg('elo'))

        labels = [entry['date'].strftime('%Y-%m-%d') for entry in data]
        elo_values = [entry['avg_elo'] for entry in data]

        class beChart(ChartJs.LineGraph):
            pass

        colors = get_colors(2)
        beChart = ChartJs.LineGraph()
        beChart.labels.grouped = labels
        beChart.data.data = elo_values
        beChart.data.label = 'Elo Blitz'
        beChart.data.borderColor = ChartJs.linear_gradient('BlitzEloCtx', colors[0], colors[1])
        beChart.options.scales['x']['ticks']['maxTicksLimit'] = 3
        beChart.options.scales['y']['beginAtZero'] = False

        BlitzElo = beChart.get()
        return BlitzElo
    
    def weekly_time():
        tactic_data = Tactic.objects.values('date__year', 'date__week').annotate(total_duration=Sum('duration'))
        game_data = Game.objects.values('date__year', 'date__week').annotate(total_duration=Sum('duration'))
        session_data = Session.objects.values('date__year', 'date__week').annotate(total_duration=Sum('duration'))
        colors = get_colors(2)

        # Unificar datos y agrupar por año y semana
        all_data = sorted(
            tactic_data.union(game_data, session_data),
            key=itemgetter('date__year', 'date__week')
        )

        grouped_data = {key: convert_minutes_to_hours(sum(entry['total_duration'] for entry in group))
                        for key, group in groupby(all_data, key=itemgetter('date__year', 'date__week'))}

        labels = [f"{year}-{week}" for year, week in grouped_data.keys()]
        total_hours = list(grouped_data.values())

        weekly_time_chart = ChartJs.BarGraph()
        weekly_time_chart.labels.grouped = labels
        weekly_time_chart.data.data = total_hours
        weekly_time_chart.data.label = 'Training Time'
        weekly_time_chart.data.backgroundColor = ChartJs.linear_gradient('WeeklyTimeCtx', colors[0], colors[1])

        WeeklyTime = weekly_time_chart.get()
        return WeeklyTime
    
   
    def ct_amount():
        tactic_data = Tactic.objects.filter(training_set='Standard').values('date__year', 'date__week').annotate(total_exercises=Sum('exercises'))
        colors = get_colors(2)

        all_data = sorted(
            tactic_data,
            key=itemgetter('date__year', 'date__week')
        )

        grouped_data = {key: sum(entry['total_exercises'] for entry in group)
                        for key, group in groupby(all_data, key=itemgetter('date__year', 'date__week'))}

        labels = [f"{year}-{week}" for year, week in grouped_data.keys()]
        total_exercises = list(grouped_data.values())

        ca_chart = ChartJs.BarGraph()
        ca_chart.labels.grouped = labels
        ca_chart.data.data = total_exercises
        ca_chart.data.label = 'CT Total Exercises'
        ca_chart.data.backgroundColor = ChartJs.linear_gradient('ctAmountCtx', colors[0], colors[1])
        ca_chart.options.scales['x']['ticks']['maxTicksLimit'] = 5

        ctAmount = ca_chart.get()
        return ctAmount

    def ct_std_perf():
        data = Tactic.objects.filter(training_set='Standard').values('date').annotate(avg_perf=Avg('performance'))
        colors = get_colors(2)

        labels = [entry['date'].strftime('%Y-%m-%d') for entry in data]
        perf_values = [entry['avg_perf'] for entry in data]

        csp_chart = ChartJs.BarGraph()
        csp_chart.labels.grouped = labels
        csp_chart.data.data = perf_values
        csp_chart.data.label = 'CT Standard Performance'
        csp_chart.data.backgroundColor = ChartJs.linear_gradient('CtStdPerfCtx', colors[0], colors[1])
        csp_chart.options.scales['x']['ticks']['maxTicksLimit'] = 3
        csp_chart.options.scales['y']['beginAtZero'] = True

        CtStdPerf = csp_chart.get()
        return CtStdPerf

    def storm_max():
        # Obtener los puntajes máximos diarios de los puzzles Storm
        data = Tactic.objects.filter(training_set='Puzzle Storm').values('date').annotate(
            max_score=Coalesce(Max('attempts__score'), 0)
        )
        colors = get_colors(2)

        # Procesar los datos para obtener las fechas y los puntajes máximos
        labels = [entry['date'].strftime('%Y-%m-%d') for entry in data]
        max_scores = [entry['max_score'] for entry in data]

        ms_chart = ChartJs.BarGraph()
        ms_chart.labels.grouped = labels
        ms_chart.data.data = max_scores
        ms_chart.data.label = 'Max Puzzle Storm Score'
        ms_chart.data.backgroundColor = ChartJs.linear_gradient('StormMaxCtx', colors[0], colors[1])
        ms_chart.options.scales['x']['ticks']['maxTicksLimit'] = 3

        StormMax = ms_chart.get()
        return StormMax
    
    def racer_max():
        data = Tactic.objects.filter(training_set='Puzzle Racer').values('date').annotate(
            max_score=Coalesce(Max('attempts__score'), 0)
        )
        colors = get_colors(2)

        # Procesar los datos para obtener las fechas y los puntajes máximos
        labels = [entry['date'].strftime('%Y-%m-%d') for entry in data]
        max_scores = [entry['max_score'] for entry in data]

        ms_chart = ChartJs.BarGraph()
        ms_chart.labels.grouped = labels
        ms_chart.data.data = max_scores
        ms_chart.data.label = 'Max Puzzle Racer Score'
        ms_chart.data.backgroundColor = ChartJs.linear_gradient('RacerMaxCtx', colors[0], colors[1])
        ms_chart.options.scales['x']['ticks']['maxTicksLimit'] = 3

        RacerMax = ms_chart.get()
        return RacerMax
    
    def racer_avg():
         # Filtrar los registros de Tactic que correspondan a Puzzle Racers
        data = Tactic.objects.filter(training_set='Puzzle Racer').values('date').annotate(
            avg_attempts=Avg('attempts__score')
        )
        colors = get_colors(2)

        # Procesar los datos para obtener las fechas y los promedios de intentos
        labels = [entry['date'].strftime('%Y-%m-%d') for entry in data]
        avg_attempts_values = [entry['avg_attempts'] for entry in data]

        # Crear gráfico de líneas o de barras según prefieras
        ar_chart = ChartJs.LineGraph()
        ar_chart.labels.grouped = labels
        ar_chart.data.data = avg_attempts_values
        ar_chart.data.label = 'Average Puzzle Racer Attempts'
        ar_chart.data.borderColor = ChartJs.linear_gradient('RacerAvgCtx', colors[0], colors[1])
        ar_chart.options.scales['x']['ticks']['maxTicksLimit'] = 5
        ar_chart.options.scales['y']['beginAtZero'] = True

        RacerAvg = ar_chart.get()
        return RacerAvg
    
    def storm_avg():
         # Filtrar los registros de Tactic que correspondan a Puzzle Racers
        data = Tactic.objects.filter(training_set='Puzzle Storm').values('date').annotate(
            avg_attempts=Avg('attempts__score')
        )
        colors = get_colors(2)

        # Procesar los datos para obtener las fechas y los promedios de intentos
        labels = [entry['date'].strftime('%Y-%m-%d') for entry in data]
        avg_attempts_values = [entry['avg_attempts'] for entry in data]

        # Crear gráfico de líneas o de barras según prefieras
        ar_chart = ChartJs.LineGraph()
        ar_chart.labels.grouped = labels
        ar_chart.data.data = avg_attempts_values
        ar_chart.data.label = 'Average Puzzle Storm Attempts'
        ar_chart.data.borderColor = ChartJs.linear_gradient('StormAvgCtx', colors[0], colors[1])
        ar_chart.options.scales['x']['ticks']['maxTicksLimit'] = 5
        ar_chart.options.scales['y']['beginAtZero'] = True

        StormAvg = ar_chart.get()
        return StormAvg

    def time_dist():
        # Calcular la fecha hace un mes desde hoy
        last_month = datetime.now() - timedelta(days=30)
        

        # Obtener datos para la distribución de tiempo en el último mes
        tactic_duration = Tactic.objects.filter(date__gte=last_month).aggregate(total_duration=Sum('duration'))['total_duration'] or 0
        game_duration = Game.objects.filter(date__gte=last_month).aggregate(total_duration=Sum('duration'))['total_duration'] or 0
        session_duration = Session.objects.filter(date__gte=last_month).aggregate(total_duration=Sum('duration'))['total_duration'] or 0

        # Procesar los datos para el gráfico de donut simple
        labels = ['Tactic', 'Game', 'Session']
        data = [tactic_duration/60, game_duration/60, session_duration/60]

        simple_donut_chart = ChartJs.PolarAreaChart()
        simple_donut_chart.labels.grouped = labels
        simple_donut_chart.data.data = data
        simple_donut_chart.data.backgroundColor = get_colors(len(labels))

        TimeDist = simple_donut_chart.get()

        return TimeDist

    def detailed_time():
        # Obtener la fecha de hace un mes desde hoy
        last_month = datetime.now() - timedelta(days=30)

        # Tactic por training_set
        tactic_data = Tactic.objects.filter(date__gte=last_month).values('training_set').annotate(
            total_duration=Sum('duration')
        )
        
        # Games por ritmo
        game_data = Game.objects.filter(date__gte=last_month).values('rithm').annotate(
            total_duration=Sum('duration')
        )

        # Sesiones por session_type
        session_data = Session.objects.filter(date__gte=last_month).values('session_type').annotate(
            total_duration=Sum('duration')
        )

        # Procesar datos para el gráfico donut combinado
        tactic_labels = [f'S - {entry["training_set"]}' for entry in tactic_data]
        tactic_durations = [entry['total_duration']/60 for entry in tactic_data]

        game_labels = [f'P - {entry["rithm"]}' for entry in game_data]
        game_durations = [entry['total_duration']/60 for entry in game_data]

        session_labels = [f'L - {entry["session_type"]}' for entry in session_data]
        session_durations = [entry['total_duration']/60 for entry in session_data]

        # Unir todas las etiquetas y duraciones
        combined_labels = tactic_labels + game_labels + session_labels
        combined_durations = tactic_durations + game_durations + session_durations

        # Obtener colores aleatorios
        combined_colors = get_colors(len(combined_labels))

        # Crear gráfico donut combinado
        combined_donut = ChartJs.PolarAreaChart()
        combined_donut.labels.grouped = combined_labels
        combined_donut.data.data = combined_durations
        combined_donut.data.backgroundColor = combined_colors
        combined_donut.options.plugins = {'legend': {'display': False}}

        DetailedTime = combined_donut.get()

        return DetailedTime
        
    
    RapidElo = rapid_elo()
    BlitzElo = blitz_elo()
    WeeklyTime = weekly_time()
    CtStdPerf = ct_std_perf()
    ctAmount = ct_amount()
    StormMax = storm_max()
    RacerMax = racer_max()
    TimeDist = time_dist()
    DetailedTime = detailed_time()
    RacerAvg = racer_avg()
    StormAvg = storm_avg()

    context = {
        "RapidElo": RapidElo,
        "BlitzElo": BlitzElo,
        "WeeklyTime": WeeklyTime,
        "CtStdPerf": CtStdPerf,
        "ctAmount": ctAmount,
        "StormMax": StormMax,
        "RacerMax": RacerMax,
        "TimeDist": TimeDist,
        "DetailedTime": DetailedTime,
        "RacerAvg": RacerAvg,
        "StormAvg": StormAvg,
        }


    return render(request, 'stats.html', context=context)


@login_required
def tactic_form(request):
    if request.method == 'POST':
        form = TacticForm(request.POST)
        if form.is_valid():
            tactic = form.save(commit=False)
            tactic.user = request.user
            tactic.save()
            return redirect('training')
    else:
        form = TacticForm()
    return render(request, 'training/tactic_form.html', {'form': form})

@login_required
def game_form(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.user = request.user
            game.save()
            return redirect('training')
    else:
        form = GameForm()
    return render(request, 'training/game_form.html', {'form': form})

@login_required
def session_form(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            return redirect('training')
    else:
        form = SessionForm()
    return render(request, 'training/session_form.html', {'form': form})









@csrf_exempt
def delete_training(request):
    if request.method == 'DELETE':
        training_id = request.GET.get('id')
        training_type = request.GET.get('type')

        if training_type == 'list-group-item-success':
            Tactic.objects.filter(id=training_id).delete()
        elif training_type == 'list-group-item-warning':
            Game.objects.filter(id=training_id).delete()
        elif training_type == 'list-group-item-info':
            Session.objects.filter(id=training_id).delete()

        # Retornar una respuesta JSON indicando el éxito de la operación
        return JsonResponse({'success': True})

    # Si la solicitud no es del tipo DELETE, retornar un error
    return JsonResponse({'success': False, 'error': 'Invalid request method'})