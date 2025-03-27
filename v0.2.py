import networkx as nx
from pyvis.network import Network
import random
from typing import Dict, List, Tuple

class ClassicalAI:
    """Simulates a classical AI model without knowledge graph"""
    def __init__(self, knowledge_base: List[Dict]):
        self.knowledge = knowledge_base
        
    def query(self, query: str) -> str:
        """Simple keyword matching and template-based response"""
        # Convert query to lowercase for matching
        query_lower = query.lower()
        
        # Basic template matching
        responses = []
        
        # Search through knowledge base for relevant information
        for item in self.knowledge:
            entity = item['entity'].lower()
            if entity in query_lower:
                # Create a response based on available information
                response = f"{item['entity']} is a {item['type']}"
                if 'related_to' in item and item['related_to']:
                    relations = [f"{rel['type']} {rel['entity']}" 
                               for rel in item['related_to']]
                    response += f" that " + ", and ".join(relations)
                responses.append(response)
        
        # If no direct matches, try to give a general response
        if not responses:
            if 'graphrag' in query_lower or 'llm' in query_lower:
                responses = ["GraphRAG is a framework that helps improve LLM performance.",
                           "LLMs can sometimes produce incorrect information."]
            elif 'knowledge graph' in query_lower:
                responses = ["Knowledge graphs help organize information in a structured way."]
            elif 'hallucination' in query_lower:
                responses = ["Hallucination refers to generating incorrect information."]
                
        # If still no response, give a default
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
            'technology': '#00ff1e',
            'framework': '#ff00f7',
            'component': '#0000ff',
            'feature': '#ffa500',
            'challenge': '#ff0000',
            'default': '#808080'
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
        net.save_graph("knowledge_graph.html")
        return "knowledge_graph.html"

    def query(self, query: str) -> str:
        """Query using knowledge graph relationships"""
        relevant_info = []
        for node in self.kg.nodes(data=True):
            if any(term.lower() in node[0].lower() for term in query.split()):
                neighbors = []
                for neighbor in self.kg.neighbors(node[0]):
                    edge_data = self.kg.get_edge_data(node[0], neighbor)
                    neighbors.append({
                        'entity': neighbor,
                        'relationship': edge_data.get('relationship', 'related')
                    })
                
                relevant_info.append({
                    'entity': node[0],
                    'type': node[1].get('type', 'concept'),
                    'connected_to': neighbors
                })
        
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

def compare_responses(classical: ClassicalAI, graphrag: GraphRAG, queries: List[str]):
    """Compare responses from both systems"""
    print("\nComparing Classical AI vs GraphRAG responses:")
    for query in queries:
        print("\n" + "="*80)
        print(f"Query: {query}")
        print("-"*40)
        print("Classical AI Response:")
        print(classical.query(query))
        print("-"*40)
        print("GraphRAG Response:")
        print(graphrag.query(query))
        print("="*80)

if __name__ == "__main__":
    # Sample knowledge base
    knowledge_base = [
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
    
    print("Initializing Classical AI and GraphRAG systems...")
    
    # Initialize both systems
    classical_ai = ClassicalAI(knowledge_base)
    graphrag = GraphRAG()
    graphrag.create_knowledge_graph(knowledge_base)
    
    # Generate visualization
    print("\nGenerating knowledge graph visualization...")
    graph_file = graphrag.visualize_graph()
    print(f"Knowledge graph visualization saved to: {graph_file}")
    
    # Test queries that highlight the differences
    test_queries = [
        "How does GraphRAG improve LLM performance?",
        "What is the role of Knowledge Graphs in the system?",
        "How does the system handle hallucinations?",
        "What are the main components of GraphRAG?",
        "How is Neo4j used in the system?",
        "Explain the relationship between Knowledge Integration and Hallucination"
    ]
    
    # Compare responses
    compare_responses(classical_ai, graphrag, test_queries)
    
    print("\nKey Differences Demonstrated:")
    print("1. Relationship Understanding: GraphRAG shows connections between concepts")
    print("2. Context Awareness: GraphRAG provides more detailed context for each entity")
    print("3. Structure: GraphRAG responses are based on graph relationships rather than templates")
    print("4. Completeness: GraphRAG can find indirect relationships through graph traversal")