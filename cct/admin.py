from django.contrib import admin
from .models import PuzzleRun, Tactic, Game, Session

admin.site.register(PuzzleRun)
admin.site.register(Tactic)
admin.site.register(Game)
admin.site.register(Session)