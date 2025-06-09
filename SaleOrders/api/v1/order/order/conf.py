http_200 = {'message': 'operation completed successfully'}
http_404 = {'message': 'object not found with slug id'}

is_status_dict = {
    'attachment_status': http_200,
    'verified': http_200,
    'cancelled': http_200,
}