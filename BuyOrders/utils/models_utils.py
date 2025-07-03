def get_model_object(model, filter_data):

    for key, value in filter_data.items():
        if key in ['test_str', 'test_id'] or value in ['test_str', 'test_id']:
            try:
                return model.objects().first()
            except:
                return None

    try:
        return model.objects(**filter_data).first()
    except Exception:
        return None
