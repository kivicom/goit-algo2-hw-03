# Building the graph with a super-source and super-sink
def build_graph():
    graph = {}
    nodes = ['Source', 'Sink', 'Термінал 1', 'Термінал 2', 'Склад 1', 'Склад 2', 'Склад 3', 'Склад 4'] + [f'Магазин {i}' for i in range(1, 15)]
    for node in nodes:
        graph[node] = {}
    
    graph['Source']['Термінал 1'] = float('inf')
    graph['Source']['Термінал 2'] = float('inf')
    graph['Термінал 1']['Source'] = 0
    graph['Термінал 2']['Source'] = 0
    
    graph['Термінал 1']['Склад 1'] = 25
    graph['Термінал 1']['Склад 2'] = 20
    graph['Термінал 1']['Склад 3'] = 15
    graph['Термінал 2']['Склад 3'] = 15
    graph['Термінал 2']['Склад 4'] = 30
    graph['Термінал 2']['Склад 2'] = 10
    
    graph['Склад 1']['Термінал 1'] = 0
    graph['Склад 2']['Термінал 1'] = 0
    graph['Склад 3']['Термінал 1'] = 0
    graph['Склад 3']['Термінал 2'] = 0
    graph['Склад 4']['Термінал 2'] = 0
    graph['Склад 2']['Термінал 2'] = 0
    
    edges = [
        ('Склад 1', 'Магазин 1', 15), ('Склад 1', 'Магазин 2', 10), ('Склад 1', 'Магазин 3', 20),
        ('Склад 2', 'Магазин 4', 15), ('Склад 2', 'Магазин 5', 10), ('Склад 2', 'Магазин 6', 25),
        ('Склад 3', 'Магазин 7', 20), ('Склад 3', 'Магазин 8', 15), ('Склад 3', 'Магазин 9', 10),
        ('Склад 4', 'Магазин 10', 20), ('Склад 4', 'Магазин 11', 10), ('Склад 4', 'Магазин 12', 15),
        ('Склад 4', 'Магазин 13', 5), ('Склад 4', 'Магазин 14', 10)
    ]
    for u, v, cap in edges:
        graph[u][v] = cap
        graph[v][u] = 0
    
    for i in range(1, 15):
        store = f'Магазин {i}'
        graph[store]['Sink'] = float('inf')
        graph['Sink'][store] = 0
    
    return graph

def bfs(graph, source, sink, parent):
    visited = {node: False for node in graph}
    queue = []
    queue.append(source)
    visited[source] = True
    
    while queue:
        u = queue.pop(0)
        for v, capacity in graph[u].items():
            if not visited[v] and capacity > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == sink:
                    return True
    return False

def edmonds_karp(graph, source, sink):
    parent = {node: None for node in graph}
    max_flow = 0
    flow_graph = {u: {v: 0 for v in graph[u]} for u in graph}
    
    while bfs(graph, source, sink, parent):
        path_flow = float('inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]
        
        max_flow += path_flow
        
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            flow_graph[u][v] += path_flow
            flow_graph[v][u] -= path_flow
            v = parent[v]
    
    return max_flow, flow_graph

def compute_terminal_to_store_flows(flow_graph):
    flows = []
    terminals = ['Термінал 1', 'Термінал 2']
    stores = [f'Магазин {i}' for i in range(1, 15)]
    warehouses = ['Склад 1', 'Склад 2', 'Склад 3', 'Склад 4']
    
    for terminal in terminals:
        for store in stores:
            total_flow = 0
            for warehouse in warehouses:
                flow_to_warehouse = flow_graph[terminal].get(warehouse, 0)
                flow_to_store = flow_graph[warehouse].get(store, 0)
                flow = min(flow_to_warehouse, flow_to_store)
                total_flow += flow
            if total_flow > 0:
                flows.append((terminal, store, total_flow))
    return flows

def generate_report():
    graph = build_graph()
    max_flow, flow_graph = edmonds_karp(graph, 'Source', 'Sink')
    flows = compute_terminal_to_store_flows(flow_graph)

    capacities = {
        ('Термінал 1', 'Склад 1'): 25, ('Термінал 1', 'Склад 2'): 20, ('Термінал 1', 'Склад 3'): 15,
        ('Термінал 2', 'Склад 3'): 15, ('Термінал 2', 'Склад 4'): 30, ('Термінал 2', 'Склад 2'): 10,
        ('Склад 1', 'Магазин 1'): 15, ('Склад 1', 'Магазин 2'): 10, ('Склад 1', 'Магазин 3'): 20,
        ('Склад 2', 'Магазин 4'): 15, ('Склад 2', 'Магазин 5'): 10, ('Склад 2', 'Магазин 6'): 25,
        ('Склад 3', 'Магазин 7'): 20, ('Склад 3', 'Магазин 8'): 15, ('Склад 3', 'Магазин 9'): 10,
        ('Склад 4', 'Магазин 10'): 20, ('Склад 4', 'Магазин 11'): 10, ('Склад 4', 'Магазин 12'): 15,
        ('Склад 4', 'Магазин 13'): 5, ('Склад 4', 'Магазин 14'): 10
    }

    report = "# Звіт про аналіз максимального потоку\n\n"
    report += "## Таблиця потоків\n\n"
    report += "| Термінал    | Магазин      | Фактичний потік (одиниць) |\n"
    report += "|-------------|--------------|---------------------------|\n"
    for terminal, store, flow in flows:
        report += f"| {terminal} | {store} | {flow} |\n"

    terminal_flows = {'Термінал 1': 0, 'Термінал 2': 0}
    for terminal, _, flow in flows:
        terminal_flows[terminal] += flow
    report += "\n## Аналіз та відповіді на запитання\n\n"
    report += "### 1. Термінали з найбільшим потоком\n"
    for terminal, total in terminal_flows.items():
        report += f"- {terminal}: {total} одиниць\n"
    max_terminal = max(terminal_flows, key=terminal_flows.get)
    report += f"**Термінал з найбільшим потоком**: {max_terminal} з {terminal_flows[max_terminal]} одиниць.\n\n"

    min_capacity_edge = min(capacities.items(), key=lambda x: x[1])
    report += "### 2. Маршрути з найменшою пропускною здатністю\n"
    report += f"Маршрут з найменшою пропускною здатністю: {min_capacity_edge[0]} з {min_capacity_edge[1]} одиниць.\n"
    report += "Ця низька пропускна здатність обмежує потік через цей маршрут, що може спричинити утворення затору. Наприклад, маршрут від Склад 4 до Магазин 13 має пропускну здатність 5 одиниць.\n\n"

    store_flows = {f'Магазин {i}': 0 for i in range(1, 15)}
    for _, store, flow in flows:
        store_flows[store] += flow
    min_store = min(store_flows.items(), key=lambda x: x[1])
    related_edges = [(u, v, cap) for (u, v), cap in capacities.items() if v == min_store[0]]
    report += "### 3. Магазини, які отримали найменше товарів\n"
    report += f"Магазин, який отримав найменше товарів: {min_store[0]} з {min_store[1]} одиниць.\n"
    report += "Пов'язані маршрути та їх пропускні здатності:\n"
    for u, v, cap in related_edges:
        report += f"- {u} -> {v}: {cap} одиниць\n"
    report += "Щоб збільшити постачання, можна підвищити пропускну здатність цих маршрутів.\n\n"

    bottlenecks = []
    for (u, v), cap in capacities.items():
        if flow_graph[u][v] == cap:
            bottlenecks.append((u, v, cap))
    report += "### 4. Визначення та усунення заторів\n"
    report += "Затори виникають там, де потік дорівнює пропускній здатності:\n"
    for u, v, cap in bottlenecks:
        report += f"- {u} -> {v}: Пропускна здатність {cap}, Потік {cap}\n"
    report += "Щоб підвищити ефективність, можна збільшити пропускну здатність цих маршрутів.\n"

    return report
