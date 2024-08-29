def translate_event_filters(filters: dict) -> dict:
    query_to_field_mapping = {
        'updated__gte': 'timestamp__gte',
        'updated__lte': 'timestamp__lte',
        'night_of_stay__gte': 'night_of_stay__gte',
        'night_of_stay__lte': 'night_of_stay__lte',
        # Add other mappings here if necessary
    }

    translated_filters = {}
    for key, value in filters.items():
        model_field = query_to_field_mapping.get(key, key)  # Default to key if no mapping exists
        translated_filters[model_field] = value
    return translated_filters
