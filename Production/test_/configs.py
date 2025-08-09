swagger_schema_url ="http://127.0.0.1:8002/api-docs/swagger.json"
access_token = open('../configs/settings/jwt/token.txt', 'r').read()
token = {
        "access_token": access_token,
        "cookies_token_keyname": "access_token"
}
ip_server = 'http://127.0.0.1:8002/api/v1'


crud_test_configs = {

    "swagger_api_schema_url": swagger_schema_url,
    "token": token,
    "ip_server": ip_server,
    "endpoints": [
        "/production-series/",
        "/production-import-product-by-car/",
        "/planning-series/",
        "/poultry-cutting-production-series/"
    ]

}

drf_test_configs = {

    "swagger_api_schema_url": swagger_schema_url,
    "token": token,
    "have_used_http_only_cookie": True,
    "ip_server": ip_server

}