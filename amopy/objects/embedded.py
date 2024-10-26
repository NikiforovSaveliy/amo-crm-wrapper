from dataclasses import dataclass

from amopy.objects.mixins import TypeValidationMixin


@dataclass
class EmbeddedLead(TypeValidationMixin):
    id: int


@dataclass
class EmbeddedContact(TypeValidationMixin):
    id: int
    is_main: bool


@dataclass
class EmbeddedCompany(TypeValidationMixin):
    id: int


@dataclass
class EmbeddedMetadataCatalogItem(TypeValidationMixin):
    id: int
    catalog_id: int
    price_id: int
    quantity: int

    def __post_init__(self):
        # Почему-то это строка в реальных запросах...
        # Несмотря на то что в доке это должно быть инт
        self.catalog_id = int(self.catalog_id)
        super().__post_init__()


@dataclass
class EmbeddedCatalogItem(TypeValidationMixin):
    id: int
    metadata: EmbeddedMetadataCatalogItem
