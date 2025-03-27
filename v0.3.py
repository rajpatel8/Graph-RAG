import networkx as nx
from pyvis.network import Network
from typing import Dict, List, Tuple

class ClassicalAI:
    """Simulates a classical AI model without knowledge graph"""
    def __init__(self, knowledge_base: List[Dict]):
        self.knowledge = knowledge_base
        
    def query(self, query: str) -> str:
        """Simple keyword matching and template-based response"""
        query_lower = query.lower()
        responses = []
        
        # Basic keyword matching
        for item in self.knowledge:
            entity = item['entity'].lower()
            if entity in query_lower:
                response = f"{item['entity']} is a {item['type']}"
                if 'related_to' in item and item['related_to']:
                    relations = [f"{rel['type']} {rel['entity']}" 
                               for rel in item['related_to']]
                    response += f" that " + ", and ".join(relations)
                responses.append(response)
        
        # If no matches, give general responses
        if not responses:
            if 'cancer' in query_lower:
                responses = ["Cancer treatments involve various drugs and therapies."]
            elif 'drug' in query_lower:
                responses = ["Different drugs have different effects on cancer cells."]
            elif 'protein' in query_lower:
                responses = ["Proteins play a role in cancer development."]
                
        if not responses:
            return "I don't have enough information to answer that query."
            
        return "\n".join(responses)

class GraphRAG:
    """Knowledge graph-based AI system"""
    def __init__(self):
        self.kg = nx.Graph()
        
    def create_knowledge_graph(self, data: List[Dict]):
        """Create a knowledge graph from structured data"""
        for item in data:
            self.kg.add_node(item['entity'], type=item['type'])
            if 'related_to' in item:
                for relation in item['related_to']:
                    self.kg.add_node(relation['entity'])
                    self.kg.add_edge(item['entity'], relation['entity'], 
                                   relationship=relation['type'])
    
    def visualize_graph(self):
        """Create interactive visualization of the knowledge graph"""
        net = Network(notebook=False, height="750px", width="100%", bgcolor="#ffffff")
        
        color_map = {
            'drug': '#00ff1e',        # Green
            'protein': '#ff00f7',     # Pink
            'pathway': '#0000ff',     # Blue
            'cancer_type': '#ffa500', # Orange
            'side_effect': '#ff0000', # Red
            'gene': '#800080',        # Purple
            'default': '#808080'      # Gray
        }
        
        for node in self.kg.nodes(data=True):
            node_type = node[1].get('type', 'default')
            color = color_map.get(node_type, color_map['default'])
            net.add_node(node[0], 
                        label=node[0], 
                        title=f"Type: {node_type}",
                        color=color)
            
        for edge in self.kg.edges(data=True):
            net.add_edge(edge[0], 
                        edge[1], 
                        title=edge[2].get('relationship', ''),
                        color='#666666')
        
        net.toggle_physics(True)
        net.show_buttons(filter_=['physics'])
        net.save_graph("cancer_research_graph.html")
        return "cancer_research_graph.html"

    def query(self, query: str) -> str:
        """Query using knowledge graph relationships"""
        relevant_info = []
        for node in self.kg.nodes(data=True):
            if any(term.lower() in node[0].lower() for term in query.split()):
                neighbors = []
                paths = []
                
                # Direct neighbors
                for neighbor in self.kg.neighbors(node[0]):
                    edge_data = self.kg.get_edge_data(node[0], neighbor)
                    neighbors.append({
                        'entity': neighbor,
                        'relationship': edge_data.get('relationship', 'related')
                    })
                
                # Find paths to related concepts (up to 2 hops)
                for target in self.kg.nodes():
                    if target != node[0]:
                        try:
                            path = nx.shortest_path(self.kg, node[0], target)
                            if len(path) <= 3:  # Only include paths up to 2 hops
                                path_info = []
                                for i in range(len(path)-1):
                                    edge_data = self.kg.get_edge_data(path[i], path[i+1])
                                    path_info.append({
                                        'from': path[i],
                                        'to': path[i+1],
                                        'relationship': edge_data.get('relationship', 'related')
                                    })
                                paths.append(path_info)
                        except nx.NetworkXNoPath:
                            continue
                
                relevant_info.append({
                    'entity': node[0],
                    'type': node[1].get('type', 'concept'),
                    'connected_to': neighbors,
                    'paths': paths
                })
        
        if relevant_info:
            response = "\nKnowledge Graph Analysis:\n"
            for info in relevant_info:
                response += f"\n• {info['entity']}"
                if info['type'] != 'concept':
                    response += f" ({info['type']})"
                response += ":\n"
                
                # Direct relationships
                if info['connected_to']:
                    response += "  Direct relationships:\n"
                    connections = [f"{n['relationship']} {n['entity']}" 
                                 for n in info['connected_to']]
                    response += "   - " + "\n   - ".join(connections) + "\n"
                
                # Multi-hop relationships
                if info['paths']:
                    response += "  Extended relationships:\n"
                    for path in info['paths']:
                        if len(path) > 1:  # Only show multi-hop paths
                            path_str = " → ".join([
                                f"{step['from']} {step['relationship']} {step['to']}"
                                for step in path
                            ])
                            response += f"   - {path_str}\n"
                
        else:
            response = "No directly relevant information found in the knowledge graph."
            
        return response

if __name__ == "__main__":
    # Sample knowledge base for cancer research
    cancer_knowledge_base = [
        {
            'entity': 'Trastuzumab',
            'type': 'drug',
            'related_to': [
                {'entity': 'HER2', 'type': 'targets'},
                {'entity': 'Breast Cancer', 'type': 'treats'},
                {'entity': 'Cardiotoxicity', 'type': 'causes'}
            ]
        },
        {
            'entity': 'HER2',
            'type': 'protein',
            'related_to': [
                {'entity': 'Cell Growth', 'type': 'regulates'},
                {'entity': 'ERBB2', 'type': 'encoded_by'}
            ]
        },
        {
            'entity': 'Breast Cancer',
            'type': 'cancer_type',
            'related_to': [
                {'entity': 'HER2', 'type': 'overexpresses'},
                {'entity': 'BRCA1', 'type': 'associated_with'}
            ]
        },
        {
            'entity': 'ERBB2',
            'type': 'gene',
            'related_to': [
                {'entity': 'PI3K Pathway', 'type': 'activates'},
                {'entity': 'Cell Growth', 'type': 'promotes'}
            ]
        },
        {
            'entity': 'PI3K Pathway',
            'type': 'pathway',
            'related_to': [
                {'entity': 'Cell Survival', 'type': 'promotes'},
                {'entity': 'Cancer Growth', 'type': 'leads_to'}
            ]
        },
        {
            'entity': 'Cardiotoxicity',
            'type': 'side_effect',
            'related_to': [
                {'entity': 'Heart Damage', 'type': 'causes'},
                {'entity': 'Dose Reduction', 'type': 'requires'}
            ]
        },
        {
            'entity': 'BRCA1',
            'type': 'gene',
            'related_to': [
                {'entity': 'DNA Repair', 'type': 'involved_in'},
                {'entity': 'Cancer Risk', 'type': 'affects'}
            ]
        }
    ]
    
    print("Initializing Classical AI and GraphRAG systems for cancer research...")
    
    # Initialize both systems
    classical_ai = ClassicalAI(cancer_knowledge_base)
    graphrag = GraphRAG()
    graphrag.create_knowledge_graph(cancer_knowledge_base)
    
    # Generate visualization
    print("\nGenerating knowledge graph visualization...")
    graph_file = graphrag.visualize_graph()
    print(f"Cancer research knowledge graph visualization saved to: {graph_file}")
    
    # Test queries that highlight the differences
    test_queries = [
        "Why is Trastuzumab effective for breast cancer?",
        "What are the risks of Trastuzumab treatment?",
        "How does HER2 relate to cancer growth?",
        "What is the relationship between ERBB2 and cancer cell growth?",
        "Why might BRCA1 mutations increase cancer risk?",
        "Explain the pathway from HER2 to cancer growth"
    ]
    
    # Compare responses
    print("\nComparing Classical AI vs GraphRAG responses:")
    for query in test_queries:
        print("\n" + "="*80)
        print(f"Query: {query}")
        print("-"*40)
        print("Classical AI Response:")
        print(classical_ai.query(query))
        print("-"*40)
        print("GraphRAG Response:")
        print(graphrag.query(query))
        print("="*80)
    
    print("\nKey Advantages of GraphRAG in Cancer Research:")
    print("1. Mechanism Understanding: Shows complete pathways from drug targets to effects")
    print("2. Risk Assessment: Identifies relationships between drugs, targets, and side effects")
    print("3. Molecular Pathways: Reveals multi-step relationships in biological processes")
    print("4. Treatment Context: Provides comprehensive view of drug interactions and effects")