from django.db.models.signals import pre_save, post_save, pre_init, post_init
from django.dispatch import receiver
from .models import FinanceRecord


# create pre_save django signal for finance record
@receiver(pre_save, sender=FinanceRecord)
def finance_record_pre_save(sender, instance, **kwargs):
    print(sender)
    print(instance)
    print('finance_record_pre_save')


# create post_save django signal for finance record
@receiver(post_save, sender=FinanceRecord)
def finance_record_post_save(sender, instance, **kwargs):
    print(sender)
    print('finance_record_post_save')
