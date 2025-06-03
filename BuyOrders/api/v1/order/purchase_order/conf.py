http_200 = {'message': 'operation completed successfully'}
http_404 = {'message': 'object not found with given id'}

set_status_400_status = lambda x: {'message': f'Object with sent slug id did not match. slug_id: <{x}>'}
status_dict = {
    'approved_by_finance': {'message': 'Purchase order successfully verified by finance'},
    'approved_by_purchaser': {'message': 'Purchase order successfully approved by purchaser'},
    'purchased': {'message': 'Purchase order successfully marked as purchased'},
}