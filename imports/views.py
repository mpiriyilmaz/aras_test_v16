# imports/views.py
from __future__ import annotations

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .registry import get_importers


def _upload_form(data=None, files=None) -> forms.Form:
    """
    Registry'deki importer'ları okuyup ChoiceField'e basan dinamik form.
    forms.py kullanmadan burada inline tanımlıyoruz ki tek dosya kalsın.
    """
    importers = get_importers()  # dict[str, ImporterClass]
    # (anahtar, görünen ad) — sınıfta label varsa onu kullan
    importer_choices = [
        (key, getattr(cls, "label", key).replace("_", " "))
        for key, cls in importers.items()
    ] or [("", "-- tanımlı importer yok --")]

    KIND_CHOICES = [("csv", "CSV"), ("xlsx", "XLSX")]

    class UploadForm(forms.Form):
        importer = forms.ChoiceField(
            label="Hedef (importer)",
            choices=importer_choices,
        )
        kind = forms.ChoiceField(
            label="Kind",
            choices=KIND_CHOICES,
            initial="csv",
        )
        sheet = forms.CharField(
            label="Sheet",
            required=False,
            help_text="Sadece XLSX için (sayfa adı veya indeks).",
        )
        file = forms.FileField(label="Dosya (CSV/XLSX)")

    return UploadForm(data=data, files=files)


@login_required
def upload(request):
    """
    CSV/XLSX yükleme ekranı.
    GET: formu gösterir
    POST: seçilen importer'ı çalıştırır (imp.run(file, kind, sheet))
    """
    if request.method == "POST":
        form = _upload_form(request.POST, request.FILES)
        if form.is_valid():
            importer_key = form.cleaned_data["importer"]
            kind = form.cleaned_data["kind"]
            sheet = form.cleaned_data.get("sheet") or None
            fh = form.cleaned_data["file"]

            importers = get_importers()
            if importer_key not in importers:
                messages.error(request, "Seçilen hedef (importer) bulunamadı.")
            else:
                imp_cls = importers[importer_key]
                imp = imp_cls()
                try:
                    added = imp.run(file=fh, kind=kind, sheet=sheet)
                except Exception as e:
                    messages.error(request, f"Yükleme başarısız: {e}")
                else:
                    cleaned_note = (
                        " (yükleme öncesi tablo temizlendi.)"
                        if getattr(imp, "replace_all", False)
                        else ""
                    )
                    messages.success(
                        request,
                        f"Yükleme tamamlandı: {added} kayıt eklendi.{cleaned_note}",
                    )
                    return redirect("imports:upload")
    else:
        form = _upload_form()

    return render(request, "imports/upload.html", {"form": form})

