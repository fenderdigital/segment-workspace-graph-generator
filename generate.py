import requests
import os

'''
    A super simple Platform API client. Error handling not included.
'''
class Client():

    URL = 'https://platform.segmentapis.com/v1beta/'

    def __init__(self, token, workspace):
        assert token != ''
        self.token = token
        self.workspace = workspace

    def get_headers(self):
        return {
            'Authorization': 'Bearer ' + self.token
        }

    def get_sources(self):
        #TODO: Loop through page_tokens
        resource = 'workspaces/' + self.workspace + '/sources'
        res = requests.get(Client.URL + resource, headers=self.get_headers(), params={ 'page_size': 100 })
        sources = res.json()['sources']
        return sources

    def get_destinations(self, source):
        #TODO: Loop through page_tokens
        res = requests.get(Client.URL + source['name'] + '/destinations', headers=self.get_headers(), params={ 'page_size': 100 })
        return res.json()['destinations']

'''
    Clean the name of one of our nodes
'''
def clean_node(name):
    chars = ' ./-[]()'
    for char in chars:
        name = name.replace(char, '_')
    return name

'''
    A very simple graph
'''
class Graph():

    def __init__(self, workspace):
        self.workspace = workspace
        self.nodes = set()
        self.edges = set()


    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, a, b):
        tup = tuple(sorted((a, b)))
        self.edges.add(tup)

    def render(self):
        print('graph ' + clean_node(self.workspace) + ' {')
        for edge in self.edges:
            print('  ' + ' -- '.join(edge))
        for node in self.nodes:
            print('  ' + node)
        print('}')


if __name__ == '__main__':
    token = os.environ['TOKEN']
    workspace = os.environ['WORKSPACE']

    client = Client(token, workspace)
    graph = Graph(workspace)
    sources = client.get_sources()
    # for some reason it seems to error on large workspaces

    for source in sources[:40]:
        name = clean_node(source['display_name'])
        destinations = client.get_destinations(source)
        graph.add_node(clean_node(name))

        for destination in destinations:
            graph.add_edge(name, clean_node(destination['display_name']))

    graph.render()
