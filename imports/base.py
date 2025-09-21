# imports/base.py
from django.db import transaction, connection

class BaseImporter:
    """
    Basit bir iskelet:
    - replace_all=True ise yükleme öncesi tabloyu TRUNCATE eder (PostgreSQL).
    - parse(file, kind, sheet) satır sözlükleri üretir.
    - to_instance(row) model instance döndürür.
    - save(instances) toplu kaydeder.
    """
    model = None
    file_kinds = ("csv", "xlsx")
    required_headers = ()
    replace_all = False  # << importer bazında aç/kapat

    # --- ÇEKİRDEK ---
    def _truncate_table(self):
        """PostgreSQL için hızlı tablo temizliği + PK sıfırlama + FK'lere CASCADE."""
        if not self.model:
            return
        table = self.model._meta.db_table
        with connection.cursor() as cur:
            cur.execute(f'TRUNCATE TABLE "{table}" RESTART IDENTITY CASCADE;')

    def run(self, file, kind: str, sheet: str | None = None) -> int:
        """Tam akış: (opsiyonel) TRUNCATE -> parse -> instance -> bulk_create."""
        with transaction.atomic():
            if self.replace_all:
                self._truncate_table()

            rows = list(self.parse(file, kind=kind, sheet=sheet))
            objects = [self.to_instance(r) for r in rows]
            self.save(objects)

        return len(objects)

    # --- Alt sınıfların dolduracağı parçalar ---
    def parse(self, file, kind: str, sheet: str | None = None):
        raise NotImplementedError

    def to_instance(self, row: dict):
        raise NotImplementedError

    def save(self, instances: list):
        # İstersen ignore_conflicts=True da verebilirsin
        self.model.objects.bulk_create(instances, batch_size=1000)

