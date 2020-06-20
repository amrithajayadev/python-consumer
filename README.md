# consumer
Pact demo consumer with pact testing class

# Prerequisite
pip install pact-python

# How to generate the PACT ?
Run the test in pacttest.py to generate the corresponding PACT json. 
Results should look like:
```
Launching unittests with arguments python -m unittest pacttest.GetPipelineInfoContract.test_get_user in C:\path\to\consumer

INFO  WEBrick 1.3.1
INFO  ruby 2.2.2 (2015-04-13) [i386-mingw32]
INFO  WEBrick::HTTPServer#start: pid=42436 port=1234


Ran 1 test in 0.231s

OK
```
# How to run the Pacts against a Service?

pact-verifier --provider-base-url=http://localhost:9099 --pact-url=./consumer-pipeline-state-manager.json --custom-provider-header="Authorization:Basic Y2lxQWRtaW46Y2lxNlRNYmEw"

Provide the URL where the provider service is running, path to where the pact json was generated, optionally provide parameters required to make a request the endpoint.
pact-verifier --help will provide all the optional parameters.

Results should look like 
```
INFO: Reading pact at ./consumer-pipeline-state-manager.json

Verifying a pact between consumer and pipeline-state-manager
  Given pipeline app info
    a request app info
      with GET /api/state
        returns a response which
WARN: Skipping set up for provider state 'pipeline app info' for consumer 'consumer' as there is no --provider-states-setup-url specified.
WARN: Adding header 'Authorization: Basic Y2lxQWRtaW46Y2lxNlRNYmEw' to replayed request. This header did not exist in the pact, and hence this test cannot confirm that the request will work in real life.
          has status code 200
          has a matching body

1 interaction, 0 failures
```
