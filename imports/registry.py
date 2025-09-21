# Tek noktadan kayıt defteri
from typing import Dict, Type

_importers: Dict[str, "BaseImporter"] = {}

def register(slug: str):
    """@register('haberlesme_kesinti') gibi kullanılacak."""
    def deco(cls):
        _importers[slug] = cls
        cls.slug = slug
        return cls
    return deco

def get_importers():
    return _importers

