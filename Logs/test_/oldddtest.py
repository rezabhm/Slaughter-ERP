# from test_.utils.endpoint_unittest import EndpointUnitTest
#
# if __name__ == '__main__':
#     data = {
#
#     "id": "6",
#     "car": {
#         "_id": "2",
#         "car": {
#             "id": 1,
#             "prefix_number": 11,
#             "alphabet": "ط",
#             "postfix_number": 111,
#             "has_refrigerator": True,
#             "slug": "1",
#             "repetitive": True,
#             "city_code": 1,
#             "product_category": {
#                 "id": 1,
#                 "name": "morgh",
#                 "slug": "1"
#             },
#             "driver": {
#                 "id": 3,
#                 "slug": "1",
#                 "contact": [
#                     {
#                         "id": 1,
#                         "name": "ali koni",
#                         "slug": "1",
#                         "unit": [
#                             {
#                                 "id": 1,
#                                 "name": "office",
#                                 "slug": "office"
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "city": {
#                 "id": 1,
#                 "name": "zanjan",
#                 "car_code": 1,
#                 "slug": "1"
#             }
#         },
#         "driver": {
#             "id": 3,
#             "slug": "1",
#             "contact": [
#                 {
#                     "id": 1,
#                     "name": "ali koni",
#                     "slug": "1",
#                     "unit": [
#                         {
#                             "id": 1,
#                             "name": "office",
#                             "slug": "office"
#                         }
#                     ]
#                 }
#             ]
#         }
#     },
#     "order_information": {
#         "_id": "3",
#         "agriculture": {
#             "id": 1,
#             "name": "sepid makian",
#             "slug": "1",
#             "city": {
#                 "id": 1,
#                 "name": "zanjan",
#                 "car_code": 1,
#                 "slug": "1"
#             }
#         },
#         "product_owner": {
#             "id": 1,
#             "slug": "1",
#             "contact": {
#                 "id": 1,
#                 "name": "ali koni",
#                 "slug": "1",
#                 "unit": [
#                     {
#                         "id": 1,
#                         "name": "office",
#                         "slug": "office"
#                     }
#                 ]
#             }
#         },
#         "slaughter_type": "Slaughterhouse delivery",
#         "order_type": "company",
#         "product": {
#             "id": 1,
#             "name": "morg",
#             "code": "12456",
#             "category": {
#                 "id": 1,
#                 "name": "morgh",
#                 "slug": "1"
#             },
#             "unit": [
#                 {
#                     "id": 1,
#                     "name": "office",
#                     "slug": "office"
#                 }
#             ],
#             "slug": "1"
#         }
#     },
#     "required_weight": 100.0,
#     "required_number": 50,
#     "weight": None,
#     "quality": None,
#     "status": "pending for verified",
#     "create": {
#         "date": "2025-06-15T08:15:58.531",
#         "user": "service_buy_orders"
#     },
#     "verified": None,
#     "received": None,
#     "finished": None,
#     "done": None,
#     "cancelled": None,
#     "price": None
# }
#     test_case = EndpointUnitTest(
#         endpoint="http://127.0.0.1:8001/api/v1/buy/production-product/s/6/",
#         method="GET",
#         token={
#             "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUyMTM1NjQ0LCJpYXQiOjE3NDk1NDM2NDQsImp0aSI6ImRiMjcyNjU3ODU1ODQ1OWQ5OGI5YjFlNDg1NTc1ZTk1IiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJyZXphIiwiZW1haWwiOiIiLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwicm9sZXMiOlt7InJvbGVfbmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIiwidW5pdHMiOlt7Im5hbWUiOiJvZmZpY2UiLCJzbHVnIjoib2ZmaWNlIn1dfV0sImlzX2FkbWluIjp0cnVlfQ.UjFgQkxoAoHBY7xvlU0aRLqr894Wb3LAlBoYZ9EwjbyDgr2f5uhdAz2qROgHWaPiGr9ek5BLWjIes9NtTDTB0DNLQsUYJsWKtKU52wGb6iI5-CMdDrAam8bHQpO02Pjg0Cj8bynatp90o_rwCUdnFJmfnqgk7-M_L5l_DzoSfg8",
#             "cookies_token_keyname": "access_token"
#         },
#         http_only_cookie=True,
#         data={},
#         expected_response={
#             "status_code": 200,
#             "body": data,
#             "compare_format": "format_checking"
#         }
#     )
#
#     test_case.run_test()
#
#     test_case = EndpointUnitTest(
#
#         **{
#             'endpoint': "http://127.0.0.1:8001/api/v1/buy/production-product/s/4/",
#             'method': "GET",
#             'token': {
#             "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUyMTM1NjQ0LCJpYXQiOjE3NDk1NDM2NDQsImp0aSI6ImRiMjcyNjU3ODU1ODQ1OWQ5OGI5YjFlNDg1NTc1ZTk1IiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJyZXphIiwiZW1haWwiOiIiLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwicm9sZXMiOlt7InJvbGVfbmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIiwidW5pdHMiOlt7Im5hbWUiOiJvZmZpY2UiLCJzbHVnIjoib2ZmaWNlIn1dfV0sImlzX2FkbWluIjp0cnVlfQ.UjFgQkxoAoHBY7xvlU0aRLqr894Wb3LAlBoYZ9EwjbyDgr2f5uhdAz2qROgHWaPiGr9ek5BLWjIes9NtTDTB0DNLQsUYJsWKtKU52wGb6iI5-CMdDrAam8bHQpO02Pjg0Cj8bynatp90o_rwCUdnFJmfnqgk7-M_L5l_DzoSfg8",
#             "cookies_token_keyname": "access_token"
#         },
#             'http_only_cookie': True,
#             'data':{},
#             'expected_response': {
#             "status_code": 404,
#             "body": {
#                 'message': "No object found with id = \"4\"."
#             }
#         },
#
#         }
#
#     )
#
#     test_case.run_test()
# from test_.utils.crud_endpoint_unittest import EndpointCRUDUnitTesting
# from test_.utils.drf_api_unittesting import DRFAPIUnitTesting
from test_.configs import crud_test_configs
from test_.utils.crud_endpoint_unittest import EndpointCRUDUnitTesting
from test_.utils.manual_unittesting import ManualEndpointUnitTesting

if __name__ == '__main__':
    #
    drf_test = DRFAPIUnitTesting(
        swagger_api_schema_url='http://127.0.0.1:8001/api-docs/swagger.json',
        token={
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUyMTM1NjQ0LCJpYXQiOjE3NDk1NDM2NDQsImp0aSI6ImRiMjcyNjU3ODU1ODQ1OWQ5OGI5YjFlNDg1NTc1ZTk1IiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJyZXphIiwiZW1haWwiOiIiLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwicm9sZXMiOlt7InJvbGVfbmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIiwidW5pdHMiOlt7Im5hbWUiOiJvZmZpY2UiLCJzbHVnIjoib2ZmaWNlIn1dfV0sImlzX2FkbWluIjp0cnVlfQ.UjFgQkxoAoHBY7xvlU0aRLqr894Wb3LAlBoYZ9EwjbyDgr2f5uhdAz2qROgHWaPiGr9ek5BLWjIes9NtTDTB0DNLQsUYJsWKtKU52wGb6iI5-CMdDrAam8bHQpO02Pjg0Cj8bynatp90o_rwCUdnFJmfnqgk7-M_L5l_DzoSfg8",
            "cookies_token_keyname": "access_token"
        },
        have_used_http_only_cookie=True,
        ip_server='http://127.0.0.1:8001/api/v1'
    )
    drf_test.run_test()

    crud_test = EndpointCRUDUnitTesting(**crud_test_configs)

    crud_test.run_test()

if __name__ == '__main__':

    json_path = 'manual_test_json\\first_test.json'
    manual_testing = ManualEndpointUnitTesting(endpoint_json_path=json_path)
    manual_testing.run_test()
