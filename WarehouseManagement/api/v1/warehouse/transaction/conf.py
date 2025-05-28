from django.utils import timezone

http_200_transaction = {'message': 'transaction successfully verified'}
http_400_transaction = {'message': 'you cant verify this transaction because ware house is not active right now.'
                               f' (date : {timezone.now()})'}
http_404_transaction = {'message': 'object didint find with your send id'}