# mutation_client.py

import http.client
import json

# Constants Copied from AppSync API 'Settings'
API_URL = "https://rwtvzb7lyzabvmrds6pdtn3bsi.appsync-api.eu-central-1.amazonaws.com"
API_KEY = "da2-c3q22dmy3fhvpj3xesbzodtqyy"

HOST = API_URL.replace('https://', '').replace('/graphql', '')

if __name__ == '__main__':
    conn = http.client.HTTPSConnection(HOST, 443)
    headers = {
        'Content-type': 'application/graphql',
        'x-api-key': API_KEY,
        'host': HOST
    }

    # Perform a query to get a Todo ID
    graphql_query = {
        'query': 'query{ tenant { items {id title} } }'
    }
    query_data = json.dumps(graphql_query)
    conn.request('POST', '/graphql', query_data, headers)
    response = conn.getresponse()

    response_string = response.read().decode('utf-8')
    print(response_string)

    # Substitue the ID in the GraphQL Mutation Variables
    response_json = json.loads(response_string)
    id = response_json['data']['listTodos']['items'][0]['id']
    new_title = "Get Lunch"

    graphql_mutation = {
        'query': 'mutation($in:UpdateTodoInput!){updateTodo(input:$in){id title}}',
        'variables': '{ "in": {"id":"' + id + '", "title":"' + new_title + '"} }'
    }
    mutation_data = json.dumps(graphql_mutation)

    # Now Perform the Mutation
    conn.request('POST', '/graphql', mutation_data, headers)
    response = conn.getresponse()

    response_string = response.read().decode('utf-8')
    print(response_string)
