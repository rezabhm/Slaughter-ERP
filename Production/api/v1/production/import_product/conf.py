from apps.production.documents import FirstStepImportCar, SecondStepImportCar, ThirdStepImportCar, FourthStepImportCar, \
    FifthStepImportCar, SixthStepImportCar, SeventhStepImportCar

set_status_400_status = lambda x: {'message': f'object with send slug id didint match. slug_id :<{x}>'}
is_status_dict = {

    'is_planned': {'message': 'object successfully planed'},
    'is_cancelled': {'message': 'object successfully cancelled'},
    'is_verified': {'message': 'object successfully verified'},
}

steps_400_status = {'message': "object didnt match with send slug id"}
steps_data = {
    1: {
        'model': FirstStepImportCar,
        'model_attribute': 'first_step',
        'data': {
            'user_date': ['entrance_to_slaughter'],
            'param': []
        },
        'status': {'message': 'step 1 successfully done.'}
    },
    2: {
        'model': SecondStepImportCar,
        'model_attribute': 'second_step',
        'data': {
            'user_date': [],
            'param': ['full_weight', 'source_weight', 'cage_number', 'product_number_per_cage']
        },
        'status': {'message': 'step 2 successfully done.'}
    },
    3: {
        'model': ThirdStepImportCar,
        'model_attribute': 'third_step',
        'data': {
            'user_date': ['start_production'],
            'param': []
        },
        'status': {'message': 'step 3 successfully done.'}
    },
    4: {
        'model': FourthStepImportCar,
        'model_attribute': 'fourth_step',
        'data': {
            'user_date': ['finish_production'],
            'param': []
        },
        'status': {'message': 'step 4 successfully done.'}
    },
    5: {
        'model': FifthStepImportCar,
        'model_attribute': 'fifth_step',
        'data': {
            'user_date': [],
            'param': [
                'empty_weight',
                'transit_losses_wight',
                'transit_losses_number',
                'losses_weight',
                'losses_number',
                'fuel',
                'extra_description'
            ]
        },
        'status': {'message': 'step 5 successfully done.'}
    },
    6: {
        'model': SixthStepImportCar,
        'model_attribute': 'sixth_step',
        'data': {
            'user_date': ['exit_from_slaughter'],
            'param': []
        },
        'status': {'message': 'step 6 successfully done.'}
    },
    7: {
        'model': SeventhStepImportCar,
        'model_attribute': 'seventh_step',
        'data': {
            'user_date': [],
            'param': ['product_slaughter_number']
        },
        'status': {'message': 'step 7 successfully done.'}
    }
}

warehouse_finish_start_200_status = {

    'production_start_date': {'message': 'production start successfully'},
    'production_finished_date': {'message': 'production finish successfully'}

}