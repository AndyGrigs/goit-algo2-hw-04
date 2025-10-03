import networkx as nx

def create_logistics_graph() -> nx.DiGraph:
    """
    Створює граф логістичної мережі
    """
    G = nx.DiGraph()
    
    edges = [
       
        # Термінал 1
        ("Термінал_1", "Склад_1", 25),
        ("Термінал_1", "Склад_2", 20),
        ("Термінал_1", "Склад_3", 15),
        
        # Термінал 2
        ("Термінал_2", "Склад_3", 15),
        ("Термінал_2", "Склад_4", 30),
        ("Термінал_2", "Склад_2", 10),
        
        
        # Склад 1
        ("Склад_1", "Магазин_1", 15),
        ("Склад_1", "Магазин_2", 10),
        ("Склад_1", "Магазин_3", 20),
        
        
        #Склад 2
        ("Склад_2", "Магазин_4", 15),
        ("Склад_2", "Магазин_5", 10),
        ("Склад_2", "Магазин_6", 25),
        
        
        #Склад 3 
        ("Склад_3", "Магазин_7", 20),
        ("Склад_3", "Магазин_8", 15),
        ("Склад_3", "Магазин_9", 10),
        
        #Склад 4 
        ("Склад_4", "Магазин_10", 20),
        ("Склад_4", "Магазин_11", 10),
        ("Склад_4", "Магазин_12", 15),
        ("Склад_4", "Магазин_13", 5),
        ("Склад_4", "Магазин_14", 10),
    ]
    
    for source, target, capacity in edges:
        G.add_edge(source, target, capacity=capacity)
    # 
    G.add_edge("SOURCE", "Термінал_1", float('inf'))
    G.add_edge("SOURCE", "Термінал_2", float('inf'))

    for i in range(1, 15):
        G.add_edge(f"Магазин_{i}", "SINK", float('inf'))

    return G


def calculate_max_flow(G: nx.DiGraph) -> tuple:
    """
    Обчислює максимальний потік від SOURCE до SINK
    
    Returns:
        (max_flow_value, flow_dict) - значення потоку та розподіл по ребрах
    """
    max_flow_value, flow_dict = nx.maximum_flow(
        G, 
        "SOURCE", 
        "SINK",
        flow_func=nx.algorithms.flow.edmonds_karp
    )
    
    return max_flow_value, flow_dict

def create_terminal_to_shop_table(flow_dict: dict) -> dict:
    """
    Створює таблицю потоків від терміналів до магазинів
    
    Returns:
        dict: {(термінал, магазин): потік}
    """
    result = {}
    
    terminals = ["Термінал_1", "Термінал_2"]
    
    for terminal in terminals:
        # Потоки від термінала до складів
        if terminal not in flow_dict:
            continue
            
        for warehouse, terminal_to_warehouse_flow in flow_dict[terminal].items():
            if terminal_to_warehouse_flow == 0:
                continue
            
            # Потоки від складу до магазинів
            if warehouse not in flow_dict:
                continue
                
            # Загальний потік зі складу
            total_from_warehouse = sum(flow_dict[warehouse].values())
            
            if total_from_warehouse == 0:
                continue
            
            # Розподіляємо потік від термінала пропорційно
            for shop, warehouse_to_shop_flow in flow_dict[warehouse].items():
                if shop.startswith("Магазин") and warehouse_to_shop_flow > 0:
                    # Пропорційний розподіл
                    proportion = warehouse_to_shop_flow / total_from_warehouse
                    flow_value = terminal_to_warehouse_flow * proportion
                    
                    key = (terminal, shop)
                    if key in result:
                        result[key] += flow_value
                    else:
                        result[key] = flow_value
    
    return result