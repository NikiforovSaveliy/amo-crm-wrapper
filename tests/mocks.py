lead_mock = {
    "id": 3912171,
    "name": "Example",
    "price": 12,
    "responsible_user_id": 504141,
    "group_id": 0,
    "status_id": 143,
    "pipeline_id": 3104455,
    "loss_reason_id": 4203748,
    "source_id": None,
    "created_by": 504141,
    "updated_by": 504141,
    "created_at": 1585299171,
    "updated_at": 1590683337,
    "closed_at": 1590683337,
    "closest_task_at": None,
    "is_deleted": False,
    "custom_fields_values": None,
    "score": None,
    "account_id": 28805383,
    "is_price_modified_by_robot": False,
    "_links": {"self": {"href": "https://example.amocrm.ru/api/v4/leads/3912171"}},
    "_embedded": {
        "tags": [
            {
                "id": 100667,
                "name": "тест",
                "color": None,
            }
        ],
        "catalog_elements": [
            {"id": 525439, "metadata": {"quantity": 1, "catalog_id": 4521}}
        ],
        "loss_reason": [
            {
                "id": 4203748,
                "name": "Пропала потребность",
                "sort": 100000,
                "created_at": 1582117280,
                "updated_at": 1582117280,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/leads/loss_reasons/4203748"
                    }
                },
            }
        ],
        "companies": [
            {
                "id": 10971463,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/companies/10971463"
                    }
                },
            }
        ],
        "contacts": [
            {
                "id": 10971465,
                "is_main": True,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/contacts/10971465"
                    }
                },
            }
        ],
    },
}
