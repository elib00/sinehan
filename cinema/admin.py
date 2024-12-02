from django.contrib import admin
from .models import Cinema, ScheduledMovie, Ticket
# Register your models here.
admin.site.register(Cinema)
# admin.site.register(NowShowingMovie)
admin.site.register(ScheduledMovie)
admin.site.register(Ticket)