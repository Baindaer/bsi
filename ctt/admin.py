from django.contrib import admin
from .models import Tactic, Game, Session

admin.site.register(Tactic)
admin.site.register(Game)
admin.site.register(Session)