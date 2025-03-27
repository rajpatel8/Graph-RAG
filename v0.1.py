import networkx as nx
from pyvis.network import Network

class SimpleGraphRAG:
    def __init__(self):
        self.kg = nx.Graph()
        
    def create_knowledge_graph(self, data):
        """Create a simple knowledge graph from structured data"""
        # Add nodes and edges from the data
        for item in data:
            self.kg.add_node(item['entity'], type=item['type'])
            if 'related_to' in item:
                for relation in item['related_to']:
                    self.kg.add_node(relation['entity'])  # Add missing nodes
                    self.kg.add_edge(item['entity'], relation['entity'], 
                                   relationship=relation['type'])
    
    def visualize_graph(self):
        """Create interactive visualization of the knowledge graph"""
        net = Network(notebook=False, height="750px", width="100%", bgcolor="#ffffff")
        
        # Color mapping for different node types
        color_map = {
            'technology': '#00ff1e',
            'framework': '#ff00f7',
            'component': '#0000ff',
            'feature': '#ffa500',
            'challenge': '#ff0000',
            'default': '#808080'
        }
        
        # Add nodes with different colors based on type
        for node in self.kg.nodes(data=True):
            node_type = node[1].get('type', 'default')
            color = color_map.get(node_type, color_map['default'])
            net.add_node(node[0], 
                        label=node[0], 
                        title=f"Type: {node_type}",
                        color=color)
            
        # Add edges with relationship labels
        for edge in self.kg.edges(data=True):
            net.add_edge(edge[0], 
                        edge[1], 
                        title=edge[2].get('relationship', ''),
                        color='#666666')
        
        # Configure physics layout
        net.toggle_physics(True)
        net.show_buttons(filter_=['physics'])
        
        # Save the graph
        net.save_graph("knowledge_graph.html")
        return "knowledge_graph.html"

    def query_with_graph(self, query):
        """Query the knowledge graph"""
        # Find relevant nodes in the graph
        relevant_info = []
        for node in self.kg.nodes(data=True):
            if any(term.lower() in node[0].lower() for term in query.split()):
                # Get connected nodes and relationships
                neighbors = []
                for neighbor in self.kg.neighbors(node[0]):
                    edge_data = self.kg.get_edge_data(node[0], neighbor)
                    neighbors.append({
                        'entity': neighbor,
                        'relationship': edge_data.get('relationship', 'related')
                    })
                
                relevant_info.append({
                    'entity': node[0],
                    'type': node[1].get('type', 'concept'),  # Add default type
                    'connected_to': neighbors
                })
        
        # Format response from graph
        if relevant_info:
            response = "\nKnowledge Graph Analysis:\n"
            for info in relevant_info:
                response += f"\n• {info['entity']}"
                if info['type'] != 'concept':
                    response += f" ({info['type']})"
                response += " is "
                if info['connected_to']:
                    connections = [f"{n['relationship']} {n['entity']}" 
                                 for n in info['connected_to']]
                    response += "connected to:\n  - " + "\n  - ".join(connections)
                else:
                    response += "an isolated concept"
                response += "\n"
        else:
            response = "No directly relevant information found in the knowledge graph."
            
        return response

# Example usage
if __name__ == "__main__":
    # Sample data for creating the knowledge graph
    sample_data = [
        {
            'entity': 'Knowledge Graphs',
            'type': 'technology',
            'related_to': [
                {'entity': 'GraphRAG', 'type': 'implements'},
                {'entity': 'Neo4j', 'type': 'uses'}
            ]
        },
        {
            'entity': 'LLMs',
            'type': 'technology',
            'related_to': [
                {'entity': 'GraphRAG', 'type': 'enhances'},
                {'entity': 'Hallucination', 'type': 'challenge'}
            ]
        },
        {
            'entity': 'GraphRAG',
            'type': 'framework',
            'related_to': [
                {'entity': 'Query Processing', 'type': 'component'},
                {'entity': 'Knowledge Integration', 'type': 'feature'}
            ]
        },
        {
            'entity': 'Query Processing',
            'type': 'component',
            'related_to': [
                {'entity': 'Knowledge Integration', 'type': 'uses'},
                {'entity': 'Neo4j', 'type': 'implements'}
            ]
        },
        {
            'entity': 'Knowledge Integration',
            'type': 'feature',
            'related_to': [
                {'entity': 'Hallucination', 'type': 'reduces'}
            ]
        },
        {
            'entity': 'Neo4j',
            'type': 'technology',
            'related_to': []
        },
        {
            'entity': 'Hallucination',
            'type': 'challenge',
            'related_to': []
        }
    ]
    
    print("Initializing GraphRAG demo...")
    demo = SimpleGraphRAG()
    
    print("Creating knowledge graph...")
    demo.create_knowledge_graph(sample_data)
    
    print("Generating visualization...")
    graph_file = demo.visualize_graph()
    print(f"Knowledge graph visualization saved to: {graph_file}")
    
    print("\nDemo Instructions:")
    print("1. Open 'knowledge_graph.html' in web browser to see the interactive visualization")
    print("2. Node colors represent different types:")
    print("   - Green: Technology")
    print("   - Pink: Framework")
    print("   - Blue: Component")
    print("   - Orange: Feature")
    print("   - Red: Challenge")
    print("3. Hover over nodes and edges to see additional information")
    print("4. Use the physics button to adjust the graph layout")
    
    print("\nTesting example queries:")
    example_queries = [
        "How does GraphRAG improve LLM performance?",
        "What is the role of Knowledge Graphs in the system?",
        "How does the system handle hallucinations?",
        "What are the main components of GraphRAG?",
        "How is Neo4j used in the system?"
    ]
    
    for query in example_queries:
        print("\n" + "="*50)
        print("Query:", query)
        result = demo.query_with_graph(query)
        print("\nResponse:", result)
        print("="*50)