from django.db.models.signals import post_save
from django.dispatch import receiver


def try_complete_order(order):
    invoices = order.invoices.all()
    if not invoices.exists():
        return
    from warehouse.models import MaterialAcceptance
    accepted_ids = set(
        MaterialAcceptance.objects.filter(invoice__order=order).values_list('invoice_id', flat=True)
    )
    if all(inv.id in accepted_ids for inv in invoices):
        order.status = 'completed'
        order.save(update_fields=['status'])
        req = order.request
        req.status = 'completed'
        req.save(update_fields=['status'])


@receiver(post_save, sender='warehouse.MaterialAcceptance')
def on_acceptance_created(sender, instance, created, **kwargs):
    if created:
        try_complete_order(instance.invoice.order)
