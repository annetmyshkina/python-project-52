from django.db import models
from django.utils.translation import gettext_lazy as _


class Labels(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name=_("Name"),
        unique=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created at")
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated at")
    )

    class Meta:
        verbose_name = _("Label")
        verbose_name_plural = _("Labels")
        ordering = ["name"]

    def __str__(self):
        return self.name
