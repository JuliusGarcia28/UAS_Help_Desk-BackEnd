from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Ticket
from .utils import create_ticket_snapshot


@receiver(pre_save, sender=Ticket)
def save_ticket_history(sender, instance, **kwargs):

    if not instance.pk:
        return

    try:
        old_ticket = Ticket.objects.get(pk=instance.pk)
    except Ticket.DoesNotExist:
        return

    fields_to_track = [
        "status",
        "priority",
    ]

    changed = False

    for field in fields_to_track:

        if getattr(old_ticket, field) != getattr(instance, field):
            changed = True
            break

    if changed:

        user = getattr(
            instance,
            "_changed_by",
            None
        )

        create_ticket_snapshot(
            old_ticket,
            user=user,
            reason="update"
        )