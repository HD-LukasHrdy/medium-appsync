# Setting up 

## Powertool GraphQL lambda 
arn:aws:lambda:eu-central-1:017000801446:layer:AWSLambdaPowertoolsPythonV2:30

### Example implementation
```python

import json
from aws_lambda_powertools.event_handler import AppSyncResolver
from typing import List
from aws_lambda_powertools import Logger

logger = Logger()
app = AppSyncResolver()

def lambda_handler(event, context):
    # Parse the event data from the GraphQL API Gateway
    print(event)
    request_data = event
    request_type = event["info"]["parentTypeName"]

    # # Depending on the query, execute the appropriate resolver function
    # if request_type == "Query":
    #     return query_resolver()
    # elif query.startswith('mutation'):
    #     return mutation_resolver(query, variables)
    # else:
    #     raise ValueError('Unsupported operation')
    
    return app.resolve(event, context)


@app.resolver(type_name="Query", field_name="tenant")
def get_tenant(
    userId: int = 0,  # noqa AA03 VNE003 shadows built-in id to match query argument, e.g., getTodo(id: "some_id")
):
    print(f"Fetching user {userId}")

    return query_resolver()


def query_resolver():
    # Replace this with your own query resolver logic
    tenants = [
        {'userId': 1, 'companyId': 1}
    ]
    return tenants[0]
    
    
@app.resolver(type_name="Mutation", field_name="addTenant")
def add_tenant(userId: int = 0, companyId: int = 0):

    tenants = [
        {'userId': userId, 'companyId': companyId}
    ]
    
    print(f"Stored new tenant: userId: {userId}, companyId: {companyId}.")

    return tenants[0]
    

@app.resolver(type_name="Mutation", field_name="batchProcessed")
def batch_processed(userId: int = 0, companyId: int = 0, molLibId: int = 0, rdkitProcessed: int = 10):
    
    print(f"Input = {molLibId}")

    moleculeLibrary = {   
            'userId': userId,
            'companyId': companyId,
            'rdkitProcessed': rdkitProcessed,
            'molLibId': molLibId,
            '__typename': 'uploadMoleculesFile'
            
        }
    
    print(f"moleculeLibrary = {molLibId}")

    return moleculeLibrary

@app.resolver(type_name="Mutation", field_name="event")
def event_received(input = None):
    
    print(f"Input = {input}")
    
    moleculeLibrary = {   
            'userId': 1,
            'companyId': 1,
            'rdkitProcessed': 10,
            'molLibId': 1,
            '__typename': input["action"]
            
        }


    return moleculeLibrary

```