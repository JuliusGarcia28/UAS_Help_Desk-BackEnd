from django.contrib import admin
from .models import Ticket, Ticket_Detail, TicketHistory


class TicketDetailInline(admin.TabularInline):
	model = Ticket_Detail
	extra = 0
	fields = ('note', 'diagnostic', 'tecnico')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	list_display = ('id', 'description', 'priority', 'status', 'cliente')
	list_filter = ('status', 'priority')
	search_fields = ('description',)
	inlines = [TicketDetailInline]


@admin.register(Ticket_Detail)
class TicketDetailAdmin(admin.ModelAdmin):
	list_display = ('id', 'ticket', 'note', 'tecnico')
	list_filter = ('tecnico',)
	search_fields = ('note',)


@admin.register(TicketHistory)
class TicketHistoryAdmin(admin.ModelAdmin):
	list_display = ('ticket_id', 'status', 'change_date', 'changed_by_email')
	list_filter = ('status',)
	search_fields = ('ticket_id',)
