import pandas as pd
import numpy as np
import networkx as nx

correlation_file = "./correlation_matrix.csv"  
correlation_matrix_df = pd.read_csv(correlation_file, index_col=0)

G = nx.from_pandas_adjacency(correlation_matrix_df)

def prim_algorithm(G):
    mst_edges = []  # Edge List of the MST
    visited = set()  # Set of visited nodes
    edges = []  # Priority queue for edges

    min_edge = None
    min_weight = float('inf')
    for u, v, data in G.edges(data=True):
        if data['weight'] < min_weight:
            min_weight = data['weight']
            min_edge = (u, v, data['weight'])

    if min_edge:
        u, v, weight = min_edge
        mst_edges.append(min_edge)
        visited.update([u, v]) 

        for neighbor, data in G[u].items():
            if neighbor not in visited:
                edges.append((data['weight'], u, neighbor))
        for neighbor, data in G[v].items():
            if neighbor not in visited:
                edges.append((data['weight'], v, neighbor))

        edges = sorted(edges)

    while edges:
        weight, u, v = edges.pop(0)

        if v not in visited:
            mst_edges.append((u, v, weight))
            visited.add(v)
            for neighbor, data in G[v].items():
                if neighbor not in visited:
                    edges.append((data['weight'], v, neighbor))
            
            edges = sorted(edges)  

    return mst_edges

mst = prim_algorithm(G)
print("Minimum Spanning Tree:")
for index, edge in enumerate(mst, start=1):
    print(f"{index}. {edge[0]} -- {edge[1]} (Weight: {edge[2]:.4f})")

def recommend_stocks_for_diversification(G, existing_stocks):
    # Stocks Validation
    if not all(stock in G.nodes for stock in existing_stocks):
        raise ValueError("Some of the existing stocks are not in the graph.")
    
    # MST for the existing portfolio
    subgraph = G.subgraph(existing_stocks)
    mst_edges = list(nx.minimum_spanning_edges(subgraph, data=True))
    mst_nodes = set(existing_stocks)

    print("Minimum Spanning Tree (MST) for the existing portfolio:")
    for u, v, data in mst_edges:
        print(f"({u}, {v}, {data['weight']})")
    
    potential_edges = []

    for node in G.nodes:
        if node not in mst_nodes:
            for mst_node in mst_nodes:
                if G.has_edge(node, mst_node):
                    weight = G[node][mst_node]['weight']
                    potential_edges.append((weight, mst_node, node))
    
    ranked_stocks = sorted(potential_edges, key=lambda x: x[0])

    unique_ranked_stocks = []
    seen_nodes = set()
    for weight, existing_stock, new_stock in ranked_stocks:
        if new_stock not in seen_nodes:
            unique_ranked_stocks.append((weight, existing_stock, new_stock))
            seen_nodes.add(new_stock)

    return unique_ranked_stocks

existing_stocks = ['BBCA', 'ANTM', 'BBRI', 'EXCL', 'ARTO']  # Example existing portfolio

recommended_stocks = recommend_stocks_for_diversification(G, existing_stocks)

print("Recommended stocks to add (sorted by suitability):")
for weight, existing_stock, new_stock in recommended_stocks:
    print(f"Stock: {new_stock}, Connected to: {existing_stock}, Correlation: {weight:.4f}")

def find_best_mst_with_minimal_top_n_sum(G, n):
    def prim_with_start_edge(G, start_edge):
        mst_edges = []
        visited = set()
        edges = []

        # Start with each edge
        u, v, weight = start_edge
        mst_edges.append(start_edge)
        visited.update([u, v])

        for neighbor, data in G[u].items():
            if neighbor not in visited:
                edges.append((data['weight'], u, neighbor))
        for neighbor, data in G[v].items():
            if neighbor not in visited:
                edges.append((data['weight'], v, neighbor))
        edges = sorted(edges) 

        while edges and len(mst_edges) < (n-1):
            weight, u, v = edges.pop(0)
            if v not in visited:
                mst_edges.append((u, v, weight))
                visited.add(v)
                for neighbor, data in G[v].items():
                    if neighbor not in visited:
                        edges.append((data['weight'], v, neighbor))
                edges = sorted(edges) 

        return mst_edges

    best_result = None
    lowest_sum = float('inf')  

    for u, v, data in G.edges(data=True):
        if u == v:  
            continue

        start_edge = (u, v, data['weight'])
        mst_edges = prim_with_start_edge(G, start_edge)

        top_n_sum = sum(edge[2] for edge in mst_edges[:n-1]) 

        if top_n_sum < lowest_sum:
            lowest_sum = top_n_sum
            best_result = {
                "starting_edge": start_edge,
                "mst_edges": mst_edges,
                "top_n_sum": top_n_sum
            }

    unique_nodes = set()
    for edge in best_result['mst_edges']:
        unique_nodes.update([edge[0], edge[1]])

    unique_nodes_sorted = sorted(unique_nodes)

    return best_result, unique_nodes_sorted

n = 10  # Adjustable N
best_mst_result, unique_nodes = find_best_mst_with_minimal_top_n_sum(G, n)

# Best Result
print(f"Best Starting Edge: {best_mst_result['starting_edge'][0]} -- {best_mst_result['starting_edge'][1]} "
      f"(Weight: {best_mst_result['starting_edge'][2]:.4f})")
print(f"Best Combination of {n} stocks in the LQ45 (9 edges):")
for index, edge in enumerate(best_mst_result['mst_edges'], start=1):
    print(f"{index}. {edge[0]} -- {edge[1]} (Weight: {edge[2]:.4f})")
print(f"Smallest Sum of First {n-1} Edge Weights: {best_mst_result['top_n_sum']:.4f}")
print(f"Unique Stocks in the Best Combination ({n} stocks): {', '.join(unique_nodes)}")

