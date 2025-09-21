from django import forms
from .registry import get_importers

class UploadForm(forms.Form):
    importer = forms.ChoiceField(choices=[], label="Hedef (importer)")
    file = forms.FileField(label="Dosya (CSV/XLSX)")
    kind = forms.ChoiceField(choices=[("csv", "CSV"), ("xlsx", "Excel (XLSX)")], initial="csv")
    sheet = forms.CharField(required=False, help_text="XLSX için sayfa adı veya index (0,1,...)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Registry’deki kayıtları şimdi oku:
        self.fields["importer"].choices = [(k, k) for k in get_importers().keys()]

