import atexit
import http
import unittest
import requests

from pact import Consumer, Provider
from requests.auth import HTTPBasicAuth

from client import get_inventory_details, save_inventory_details

pact = Consumer('consumer').has_pact_with(Provider('python-producer'), pact_dir='./pacts')
pact.start_service()
atexit.register(pact.stop_service)
host = 'https://yourpactbroker.domain.com:8443'
broker_url = '{host}/pacts/provider/{provider}/consumer/{consumer}/version/{consumerApplicationVersion}'.format(host=host,
    provider='python-producer', consumer='consumer', consumerApplicationVersion='1.0.0')


def _publish_to_broker(pactfile):
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    resp = requests.put(broker_url, data=open(pactfile, 'rb'), headers=headers, auth=HTTPBasicAuth('uname', 'password'), verify=False)
    if resp.status_code == http.HTTPStatus.OK:
        print('Template has been published.')
    else:
        print('Unable to publish template.')
        print(resp.status_code)


class GetPipelineInfoContract(unittest.TestCase):
    def test_get_inventory(self):
        expected = dict(productName="Laptops", locationName="Bangalore", quantity=1000)

        (pact
         .given('inventory exists')
         .upon_receiving('a request to get inventory')
         .with_request('get', '/api/inventory')
         .will_respond_with(200, body=expected))

        with pact:
            result = get_inventory_details()

        self.assertEqual(result, expected)
        # _publish_to_broker('consumer-pipeline-state-manager.json')

    def test_save_inventory(self):
        headers = {'Content-type': 'application/json'}
        expected = {"productName": "Laptops", "locationName": "Bangalore", "quantity": 1000}

        (pact
         .given('create inventory')
         .upon_receiving('a request to save inventory')
         .with_request('post', '/api/inventory', body=expected, headers=headers)
         .will_respond_with(200, body=expected, headers=headers))

        with pact:
            result = save_inventory_details()

        self.assertEqual(result, expected)

    @unittest.skip("skipping for now because amqp provider not implemented")
    def test_rabbit(self):
        headers = {'Content-type': 'application/json'}
        expected = {"productName": "Laptops", "locationName": "Bangalore", "quantity": 1000}
        (pact
         .given('default')
         .upon_receiving('message for python')
         .with_request('get', '/rabbitmq/producer', query=expected, headers=headers)
         .will_respond_with(200, body=expected))

        with pact:
            result = save_inventory_details()

        self.assertEqual(result, expected)
        # _publish_to_broker('consumer-pipeline-state-manager.json')

    def tearDown(self):
        _publish_to_broker('pacts/consumer-python-producer.json')
