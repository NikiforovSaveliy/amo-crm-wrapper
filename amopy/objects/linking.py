from dataclasses import dataclass
from typing import Literal, Optional

from amopy.objects.mixins import TypeValidationMixin


@dataclass
class LinkingItemMetadata(TypeValidationMixin):
    quantity: int
    catalog_id: int


@dataclass
class LinkingItem(TypeValidationMixin):
    to_entity_id: int
    to_entity_type: Literal[
        "leads", "contacts", "companies", "customers", "catalog_elements"
    ]
    metadata: Optional[LinkingItemMetadata]
