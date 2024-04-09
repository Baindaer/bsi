from django import forms
from .models import Tactic, Game, Session, TacticAttempt
from datetime import date


class TacticForm(forms.ModelForm):

    SET_CHOICES = [
        ('Standard', 'Standard'),
        ('Endgame', 'Endgame'),
        ('Woodpecker', 'Woodpecker'),
        ('Puzzle Storm', 'Puzzle Storm'),
        ('Puzzle Racer', 'Puzzle Racer'),
        ('Aimchess Routine', 'Aimchess Routine'),
        ('Daily Challenge', 'Daily Challenge'),
        ('Focus Workout', 'Focus Workout'),
    ]

    score = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ''}), required=False)
    exercises = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ''}), required=False)
    performance = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ''}), required=False)
    training_set = forms.ChoiceField(choices=SET_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': ''}))
    duration = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))


    class Meta:
        model = Tactic
        fields = ['score', 'exercises', 'performance', 'training_set', 'duration', 'date']

    def __init__(self, *args, **kwargs):
        super(TacticForm, self).__init__(*args, **kwargs)
        # Establecer la fecha actual como valor predeterminado para el campo date
        self.initial['date'] = date.today()
        self.initial['duration'] = 2

class TacticAttemptForm(forms.ModelForm):

    score = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ''}))
    tactic = forms.ModelChoiceField(queryset=Tactic.objects.all())

    class Meta:
        model = TacticAttempt
        fields = ['score', 'tactic']

    def __init__(self, *args, **kwargs):
        super(TacticAttemptForm, self).__init__(*args, **kwargs)

        self.fields['tactic'].widget.attrs['class'] = 'form-control'

class GameForm(forms.ModelForm):

    RITHM_CHOICES = [
        ('Bullet', 'Bullet'),
        ('Blitz', 'Blitz'),
        ('Rapid', 'Rapid'),
        ('Classic', 'Classic'),
    ]

    PLATAFORM_CHOICES = [
        ('Chess.com', 'Chess.com'),
        ('Lichess', 'Lichess'),
        ('OTB', 'OTB'),
    ]

    rithm = forms.ChoiceField(choices=RITHM_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': ''}))
    score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ''}))
    games = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ''}))
    elo = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ''}))
    duration = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), required=False)
    plataform = forms.ChoiceField(choices=PLATAFORM_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': ''}))
    # otb = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control form-check-input', 'type': 'checkbox', 'role': 'switch'}), required=False)


    class Meta:
        model = Game
        fields = ['rithm', 'score', 'games', 'elo', 'duration', 'date', 'link', 'plataform']

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        # Establecer la fecha actual como valor predeterminado para el campo date
        self.initial['date'] = date.today()
        self.initial['plataform'] = 'Chess.com'
        self.initial['duration'] = 6
        self.initial['rithm'] = 'Blitz'
    

class SessionForm(forms.ModelForm):

    SESSION_CHOICES = [
        ('Opening', 'Opening'),
        ('Strategy', 'Strategy'),
        ('Game Analysis', 'Game Analysis'),
        ('Endgame', 'Endgame'),
        ('Workout', 'Workout'),
    ]

    session_type = forms.ChoiceField(choices=SESSION_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': ''}))
    theme = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'type': 'text', 'rows': 3}), required=False)
    duration = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))


    class Meta:
        model = Session
        fields = ['session_type', 'theme', 'duration', 'date', 'notes']

    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        # Establecer la fecha actual como valor predeterminado para el campo date
        self.initial['date'] = date.today()
        self.initial['duration'] = 60
