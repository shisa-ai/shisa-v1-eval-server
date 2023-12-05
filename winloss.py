import sqlite3
from   pprint import pprint
from tabulate import tabulate

conn = sqlite3.connect('eval-2.db')

# Get models
result = conn.execute("SELECT name FROM models WHERE name in ('shisa-mega-7b-v1.2', 'shisa-mega-dpo-7b-v1.1')").fetchall()
models = {} 
for r in result:
    models[r[0]] = { 'win': 0, 'loss': 0, 'draw': 0}

result = conn.execute("SELECT * FROM matches ORDER by updated ASC").fetchall()

for r in result:
    model_1 = r[0]
    model_2 = r[1]
    mr = r[2]

    if mr == 'win':
        models[model_1]['win'] += 1
        models[model_2]['loss'] += 1
    elif mr == 'loss':
        models[model_1]['loss'] += 1
        models[model_2]['win'] += 1
    elif mr == 'draw':
        models[model_1]['draw'] += 1
        models[model_2]['draw'] += 1

for m in models:
    model = models[m]
    total = model['win'] + model['loss'] + model['draw']
    model['wpct'] = 100 * model['win'] / total
    model['wdpct'] = 100 * (model['win'] + model['draw']) / total


# Convert dict of dicts to a list of dicts with the key included
formatted_data = [
    {'model': key, 'wpct': f"{value['wpct']:.2f}", 'wdpct': f"{value['wdpct']:.2f}", 'win': value['win'], 'loss': value['loss'], 'draw': value['draw']} 
    for key, value in models.items()
]
# Sort by a specific attribute
sorted_data = sorted(formatted_data, key=lambda x: x['wdpct'], reverse=True)
pprint(sorted_data)

columns = ['model', 'wpct', 'wdpct', 'win', 'loss', 'draw']

print(tabulate(sorted_data, headers='keys'))
# print(tabulate(sorted_data, headers=columns))

'''
for model in sorted(i.getRatingList(), key=lambda x: x[1], reverse=True):
    print(f'{model[0].ljust(22)} : {model[1]:7.2f}')
'''
