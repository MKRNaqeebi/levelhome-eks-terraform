
import requests

server_url = "http://127.0.0.1:8000"

def test_get_products():
    response = requests.get(server_url + "/products")
    assert 200 == response.status_code

def test_delete_products():
    response = requests.delete(server_url + "/products/prod_test")
    assert 202 == response.status_code
    assert '"product deleted successfully"' == response.text

def test_delete_products_not_found():
    response = requests.delete(server_url + "/products/prod_404")
#    assert 404 == response.status_code
    assert '"product not found"' == response.text


def test_create_products():
    product_payload = {'product_id':'prod_test', 'product_name':'p_test_name', 'product_description':'prod_test_des', 'product_price': 12.36}
    request_headers=""
    response = requests.post(server_url + "/products",json=product_payload)
    assert 201 == response.status_code
    assert '"product inserted successfully"' == response.text
