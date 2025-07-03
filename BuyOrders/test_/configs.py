swagger_schema_url ="http://127.0.0.1:8001/api-docs/swagger.json"
access_token = open('..\\configs\\settings\\jwt\\token.txt', 'r').read()
token = {
        "access_token": access_token,
        "cookies_token_keyname": "access_token"
}
ip_server = 'http://127.0.0.1:8001/api/v1/buy'


crud_test_configs = {

    "swagger_api_schema_url": swagger_schema_url,
    "token":token,
    "ip_server": ip_server,
    "endpoints": [

        "/production-product/"
    ]

}

drf_test_configs = {

    "swagger_api_schema_url": swagger_schema_url,
    "token": token,
    "have_used_http_only_cookie": True,
    "ip_server": ip_server

}