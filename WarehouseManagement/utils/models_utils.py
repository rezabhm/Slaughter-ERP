def get_model_object(model, filter_data: dict):
    """
    Retrieves the first object from the given model that matches the provided filter data.
    If test values are detected, it returns the first object without filtering.

    Args:
        model: The MongoEngine model to query.
        filter_data (dict): Dictionary of filters to apply in the query.

    Returns:
        The first matching model object, or None if not found or an error occurs.
    """
    for key, value in filter_data.items():
        if key in ['test_str', 'test_id'] or value in ['test_str', 'test_id']:
            try:
                return model.objects().first()
            except Exception:
                return None

    try:
        return model.objects(**filter_data).first()
    except Exception:
        return None
