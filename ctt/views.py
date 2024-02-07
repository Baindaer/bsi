from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Sum, Avg
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from itertools import groupby
from operator import attrgetter, itemgetter

from .forms import PuzzleRunForm, TacticForm, GameForm, SessionForm
from .models import PuzzleRun, Tactic, Game, Session

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
    puzzle_runs = PuzzleRun.objects.all()
    tactics = Tactic.objects.all()
    games = Game.objects.all()
    sessions = Session.objects.all()


    # Combinar todos los entrenamientos en una lista
    all_training = list(puzzle_runs) + list(tactics) + list(games) + list(sessions)

    # Agrupar los entrenamientos por fecha
    all_training.sort(key=attrgetter('date'), reverse=True)
    grouped_training = {date: {'trainings': list(group)} for date, group in groupby(all_training, key=attrgetter('date'))}
     # Calcular la duración total para cada fecha
    for date, training_list in grouped_training.items():
        total_duration = sum(training.duration for training in training_list['trainings'])
        grouped_training[date]['total_duration'] = round(total_duration / 60, 1)



    # Renderizar la plantilla con los datos
    return render(request, 'training.html', {
        'puzzle_runs': puzzle_runs,
        'tactics': tactics,
        'games': games,
        'sessions': sessions,
        'grouped_training': grouped_training,
    })



@login_required
def training_dashboard(request):
    return render(request, 'training/dashboard.html')

@login_required
def stats_view(request):

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

        be_chart = ChartJs.LineGraph()
        be_chart.labels.grouped = labels
        be_chart.data.data = elo_values
        be_chart.data.label = 'Elo Rapid'
        be_chart.data.borderColor = ChartJs.linear_gradient('RapidEloCtx', Color.Blue, Color.Magenta)
        be_chart.options.scales['x']['ticks']['maxTicksLimit'] = 3

        rapidElo = be_chart.get()
        return rapidElo
    
    def blitz_elo():
        data = Game.objects.filter(rithm='Blitz', plataform='Chess.com').values('date').annotate(avg_elo=Avg('elo'))

        labels = [entry['date'].strftime('%Y-%m-%d') for entry in data]
        elo_values = [entry['avg_elo'] for entry in data]

        be_chart = ChartJs.LineGraph()
        be_chart.labels.grouped = labels
        be_chart.data.data = elo_values
        be_chart.data.label = 'Elo Blitz'
        be_chart.data.borderColor = ChartJs.linear_gradient('BlitzEloCtx', Color.Magenta, Color.Blue)
        be_chart.options.scales['x']['ticks']['maxTicksLimit'] = 3

        BlitzElo = be_chart.get()
        return BlitzElo
    
    def weekly_time():
        puzzle_run_data = PuzzleRun.objects.values('date__year', 'date__week').annotate(total_duration=Sum('duration'))
        tactic_data = Tactic.objects.values('date__year', 'date__week').annotate(total_duration=Sum('duration'))
        game_data = Game.objects.values('date__year', 'date__week').annotate(total_duration=Sum('duration'))
        session_data = Session.objects.values('date__year', 'date__week').annotate(total_duration=Sum('duration'))

        # Unificar datos y agrupar por año y semana
        all_data = sorted(
            puzzle_run_data.union(tactic_data, game_data, session_data),
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
        weekly_time_chart.data.backgroundColor = ChartJs.linear_gradient('WeeklyTimeCtx', Color.Blue, Color.Green)

        WeeklyTime = weekly_time_chart.get()
        return WeeklyTime
    
    def ct_std_perf():
        data = Tactic.objects.filter(training_set='Standard').values('date').annotate(avg_perf=Avg('performance'))

        labels = [entry['date'].strftime('%Y-%m-%d') for entry in data]
        perf_values = [entry['avg_perf'] for entry in data]

        csp_chart = ChartJs.LineGraph()
        csp_chart.labels.grouped = labels
        csp_chart.data.data = perf_values
        csp_chart.data.label = 'CT Standard Performance'
        csp_chart.data.borderColor = ChartJs.linear_gradient('CtStdPerfCtx', Color.Cyan, Color.Yellow)
        csp_chart.options.scales['x']['ticks']['maxTicksLimit'] = 3

        CtStdPerf = csp_chart.get()
        return CtStdPerf

    def ct_amount():
        tactic_data = Tactic.objects.values('date__year', 'date__week').annotate(total_exercises=Sum('exercises'))

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
        ca_chart.data.backgroundColor = ChartJs.linear_gradient('CtStdPerfCtx', Color.Green, Color.Magenta)
        ca_chart.options.scales['x']['ticks']['maxTicksLimit'] = 5

        ctAmount = ca_chart.get()
        return ctAmount

        
    
    RapidElo = rapid_elo()
    BlitzElo = blitz_elo()
    WeeklyTime = weekly_time()
    CtStdPerf = ct_std_perf()
    ctAmount = ct_amount()

    context = {
        "RapidElo": RapidElo,
        "BlitzElo": BlitzElo,
        "WeeklyTime": WeeklyTime,
        "CtStdPerf": CtStdPerf,
        "ctAmount": ctAmount,
        }


    return render(request, 'stats.html', context=context)

@login_required
def puzzle_run_form(request):
    if request.method == 'POST':
        form = PuzzleRunForm(request.POST)
        if form.is_valid():
            puzzle_run = form.save(commit=False)
            puzzle_run.user = request.user
            puzzle_run.save()
            return redirect('training_dashboard')
    else:
        form = PuzzleRunForm()
    return render(request, 'training/puzzle_run_form.html', {'form': form})

@login_required
def tactic_form(request):
    if request.method == 'POST':
        form = TacticForm(request.POST)
        if form.is_valid():
            tactic = form.save(commit=False)
            tactic.user = request.user
            tactic.save()
            return redirect('training_dashboard')
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
            return redirect('training_dashboard')
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
            return redirect('training_dashboard')
    else:
        form = SessionForm()
    return render(request, 'training/session_form.html', {'form': form})









def delete_training(request):
    training_id = request.GET.get('id')
    training_type = request.GET.get('type')

    # Lógica para eliminar el entrenamiento según el tipo
    if training_type == 'list-group-item-primary':
        PuzzleRun.objects.filter(id=training_id).delete()
    elif training_type == 'list-group-item-success':
        Tactic.objects.filter(id=training_id).delete()
    elif training_type == 'list-group-item-warning':
        Game.objects.filter(id=training_id).delete()
    elif training_type == 'list-group-item-info':
        Session.objects.filter(id=training_id).delete()

    # Redirigir a la página de entrenamientos después de la eliminación
    return redirect('training')