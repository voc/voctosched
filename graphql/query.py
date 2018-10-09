import requests

# Adapted from https://gist.github.com/gbaman/b3137e18c739e0cf98539bf4ec4366ad

def run_query(apiurl, query):
    request = requests.post(apiurl, json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))