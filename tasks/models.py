from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Tasks(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name=_('Name')
    )

    description = models.TextField(
        verbose_name=_('Description')
    )

    status = models.ForeignKey(
        'statuses.Statuses',
        on_delete=models.PROTECT,
        verbose_name=_('Status')
    )

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='authored_tasks',
        verbose_name=_('Author')
    )

    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executed_tasks',
        null=True,
        blank=True,
        verbose_name=_('Executor')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at')
    )

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['id']

    def __str__(self):
        return self.name

    def clean(self):
        if self.executor and not User.objects.filter(pk=self.executor.pk).exists():
            raise ValidationError({'executor': 'The specified performer does not exist'})


