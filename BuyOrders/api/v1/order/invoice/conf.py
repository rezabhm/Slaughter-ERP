http_200 = {'message': 'Operation completed successfully'}
http_404 = {'message': 'Object with sent slug id did not match'}

set_status_400_status = lambda x: {'message': f'Object with sent slug id did not match. slug_id: <{x}>'}
status_dict = {
    'add_purchase_orders': {'message': 'Purchase orders successfully added to invoice'}
}