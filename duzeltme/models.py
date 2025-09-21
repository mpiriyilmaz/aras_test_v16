# duzeltme/models.py
from django.db import models
from core.fields import DateTimeSecField  # <-- custom field

class HaberlesmeKesinti(models.Model):
    modem = models.CharField(max_length=64, db_index=True)
    baslangic = DateTimeSecField()
    bitis     = DateTimeSecField()
    sure      = models.IntegerField()
    created_at = DateTimeSecField(auto_now_add=True)

    class Meta:
        verbose_name = "Haberleşme Kesinti"
        verbose_name_plural = "Haberleşme Kesintileri"
        constraints = [
            models.UniqueConstraint(
                fields=["modem", "baslangic", "bitis"],
                name="uniq_modem_baslangic_bitis",
            )
        ]

    def __str__(self):
        return f"{self.modem} | {self.baslangic} → {self.bitis}"

