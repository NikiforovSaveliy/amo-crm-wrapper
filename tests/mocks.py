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
contact_mock = {
    "id": 3,
    "name": "Иван Иванов",
    "first_name": "Иван",
    "last_name": "Иванов",
    "responsible_user_id": 504141,
    "group_id": 0,
    "created_by": 504141,
    "updated_by": 504141,
    "created_at": 1582117331,
    "updated_at": 1590943929,
    "closest_task_at": None,
    "custom_fields_values": [
        {
            "field_id": 3,
            "field_name": "Телефон",
            "field_code": "PHONE",
            "field_type": "multitext",
            "values": [{"value": "+79123", "enum_id": 1, "enum_code": "WORK"}],
        }
    ],
    "account_id": 28805383,
    "_embedded": {
        "tags": [],
        "leads": [
            {
                "id": 1,
                "_links": {
                    "self": {"href": "https://example.amocrm.ru/api/v4/leads/1"}
                },
            },
            {
                "id": 3916883,
                "_links": {
                    "self": {"href": "https://example.amocrm.ru/api/v4/leads/3916883"}
                },
            },
        ],
        "customers": [
            {
                "id": 134923,
                "_links": {
                    "self": {
                        "href": "https://example.amocrm.ru/api/v4/customers/134923"
                    }
                },
            }
        ],
        "catalog_elements": [],
        "companies": [
            {
                "id": 1,
                "_links": {
                    "self": {"href": "https://example.amocrm.ru/api/v4/companies/1"}
                },
            }
        ],
    },
}

lead_with_custom_fields_mock = {
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
            }
        ],
        "companies": [{"id": 10971463}],
        "contacts": [{"id": 10971465, "is_main": True}],
    },
}
