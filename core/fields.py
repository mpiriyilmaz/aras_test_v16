# core/fields.py
from django.db import models

class DateTimeSecField(models.DateTimeField):
    """
    PostgreSQL'de her zaman 'timestamp(0) without time zone' üretir
    (saniye hassasiyetinde, tz'siz). Diğer veritabanlarında
    varsayılan tipe düşer.
    """
    def db_type(self, connection):
        if connection.vendor == "postgresql":
            return "timestamp(0) without time zone"
        return super().db_type(connection)

