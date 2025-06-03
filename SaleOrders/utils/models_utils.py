def get_model_object(model, filter_data):

    try:
        return model.objects(**filter_data).first()
    except Exception:
        return None
