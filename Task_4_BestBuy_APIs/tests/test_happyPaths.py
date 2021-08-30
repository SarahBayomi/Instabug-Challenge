import os
import requests
import json
import jsonpath

# API URL
url = 'http://localhost:3030'


# /version test
# 1) Validate status and version
def test_version():
    version = url + '/version'
    response = requests.get(version)
    response_get_json = response.json()
    version = jsonpath.jsonpath(response_get_json, 'version')
    # validate status code:
    assert response.status_code == 200
    # validate json response
    assert version[0] == '1.1.0'

# /healthcheck test
# 2) Validate status and numbers for products, stores and categories as a health check
def test_healthCheck():
    healthCheck = url + '/healthcheck'
    response = requests.get(healthCheck)
    response_get_json = response.json()
    documents = jsonpath.jsonpath(response_get_json, 'documents')
    products_number = documents[0]['products']
    stores = documents[0]['stores']
    categories = documents[0]['categories']
    # validate status code:
    assert response.status_code == 200
    # validate json response
    assert products_number == 51957
    assert stores == 1561
    assert categories == 4307


# /products tests
# 3) Validate getting the whole list of products
def test_products():
    products = url + '/products'
    response = requests.get(products)
    response_get_json = response.json()
    total_products = jsonpath.jsonpath(response_get_json, 'total')
    # validate status code:
    assert response.status_code == 200
    # validate the products number:
    assert total_products[0] == 51957

# 4) Validate the fields of each product is existed
def test_products_fields():
    products = url + '/products/?$limit=51957'
    response = requests.get(products)
    response_get_json = response.json()
    data = jsonpath.jsonpath(response_get_json, 'data')
    # Range is to 25 as this is the limit for the products to be retrieved
    for i in range(0, 25):
        product = data[0][i]
        # Get fields
        id = jsonpath.jsonpath(product, 'id')
        name = jsonpath.jsonpath(product, 'name')
        type = jsonpath.jsonpath(product, 'type')
        price = jsonpath.jsonpath(product, 'price')
        upc = jsonpath.jsonpath(product, 'upc')
        shipping = jsonpath.jsonpath(product, 'shipping')
        description = jsonpath.jsonpath(product, 'description')
        manufacturer = jsonpath.jsonpath(product, 'manufacturer')
        model = jsonpath.jsonpath(product, 'model')
        URL = jsonpath.jsonpath(product, 'url')
        image = jsonpath.jsonpath(product, 'image')
        categories = jsonpath.jsonpath(product, 'categories')
        # Asserting existence of these fields
        assert id is True
        assert name is True
        assert type is True
        assert price is True
        assert upc is True
        assert shipping is True
        assert description is True
        assert manufacturer is True
        assert model is True
        assert URL is True
        assert image is True
        assert categories is True

# /services
# 5) Validate end to end scenario for service
def test_CRUD_service():
    services = url + '/services'
    # Read input json file
    file = open(os.getcwd() + "\\createService.json", 'r')
    json_input = file.read()
    request_json = json.loads(json_input)
    # POST the new service
    response = requests.post(services, request_json)
    assert response.status_code == 201
    id = jsonpath.jsonpath(response.json(), 'id')
    id = id[0]
    # Get this new created service
    new_service = services + '/' + str(id)
    response = requests.get(new_service)
    assert response.status_code == 200
    # Update this new created service
    file = open(os.getcwd() + "\\updateService.json", 'r')
    json_input = file.read()
    request_json = json.loads(json_input)
    response = requests.put(new_service, request_json)
    assert response.status_code == 200
    # Delete this new created service
    response = requests.delete(new_service)
    assert response.status_code == 200

# /stores
# 6) Filter stores with a certain state and list only name, address and state
def test_stores_state():
    stores = url + '/stores?state=MN&$select[]=name&$select[]=address&$select[]=state'
    response = requests.get(stores)
    assert response.status_code == 200
    # Validate that the result is with expected state
    response_get_json = response.json()
    data = jsonpath.jsonpath(response_get_json, 'data')
    for i in range(0, 10):
        product = data[0][i]
        # Get state
        state = jsonpath.jsonpath(product, 'state')
        assert state[0] == 'MN'
