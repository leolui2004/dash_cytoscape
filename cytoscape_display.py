# https://stackoverflow.com/questions/57143087/pygraphviz-oserror-format-dot-not-recognized-use-one-of
# sudo apt install graphviz-dev

import dash
import dash_cytoscape as cyto
import dash_html_components as html
import networkx as nx
import csv

twitter_dict = {"micaholic1981":"Ai","aimyonGtter":"あいみょん","CcAwesome":"Awesome City Club","mone_tohoent":"上白石萌音",
                "sakurazaka46":"櫻坂46","nekoyanagi_line":"東京事変","NiziU__official":"NiziU","nogizaka46":"乃木坂46","Perfume_Staff":"Perfume",
                "BiSHidol":"BiSH","hinatazaka46":"日向坂46","MISIA":"MISIA","milet_music":"milet",
                "mllnnmprd":"millennium parade","KIKI_526":"Belle（中村佳穂）","YOASOBI_staff":"YOASOBI","LiSA_OLiVE":"LiSA"}

twitter_lists = []
for twitter_list in twitter_dict.keys():
    twitter_lists.append(twitter_dict[twitter_list])

node_attrs = {}
center_to_followers = {}

for screenname in twitter_dict.keys():
    node_attrs[screenname] = {}
    node_attrs[screenname]['name'] = twitter_dict[screenname]

for screenname in twitter_dict.keys():
    twitter_followers = []
    with open(f'product/{screenname}.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            twitter_followers.append(row[0])
            if row[0] not in node_attrs:
                node_attrs[row[0]] = {}
                node_attrs[row[0]]['name'] = row[0]
    center_to_followers[screenname] = twitter_followers

graph = nx.from_dict_of_lists(center_to_followers)
nx.set_node_attributes(graph, node_attrs)

'''transfer'''
pos = nx.nx_agraph.graphviz_layout(graph)
pos_list = []
for value in pos.values():
    pos_list.append({'x': value[0] * 10, 'y': value[1] * 10})

cy = nx.readwrite.json_graph.cytoscape_data(graph)
for i in range(len(cy['elements']['nodes'])):
    cy['elements']['nodes'][i]['data']['label'] = cy['elements']['nodes'][i]['data']['name']
    cy['elements']['nodes'][i]['position'] = pos_list[i]
    if cy['elements']['nodes'][i]['data']['label'] in twitter_lists:
        cy['elements']['nodes'][i]['classes'] = 'red triangle'

elements_list = []
for j in cy['elements']['nodes']:
    elements_list.append(j)
for k in cy['elements']['edges']:
    elements_list.append(k)

'''dash'''
app = dash.Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'preset'},
        style={'width': '2160px', 'height': '1440px'},
        elements=elements_list
    )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)