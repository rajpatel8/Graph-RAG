import os
import networkx as nx
from pyvis.network import Network
import requests
import time
from typing import Dict, List, Tuple
from openai import OpenAI

class ClassicalAI:
    """Classical AI using OpenAI API"""
    def __init__(self, knowledge_base: List[Dict]):
        self.knowledge = knowledge_base
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def raw_query(self, query: str) -> str:
        """Query using only basic knowledge base"""
        try:
            # Format context
            context = "Medical Knowledge Base:\n\n"
            for item in self.knowledge:
                context += f"• {item['entity']} ({item['type']}):\n"
                if 'related_to' in item and item['related_to']:
                    for rel in item['related_to']:
                        context += f"  - {rel['type']} {rel['entity']}\n"
                context += "\n"
            
            prompt = f"""Based on the following medical knowledge base, please provide a detailed and accurate answer:

{context}

Question: {query}

Please provide a clear and specific answer focusing on the medical relationships and mechanisms involved."""

            return self._make_api_call(prompt)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def query_with_graph_context(self, query: str, graph_context: str) -> str:
        """Query using GraphRAG context"""
        try:
            prompt = f"""As a medical expert, analyze this knowledge graph data:

{graph_context}

Question: {query}

Based on the knowledge graph relationships shown above, provide a comprehensive explanation that:
1. Explains the key relationships
2. Describes the biological mechanisms
3. Highlights the clinical implications

Focus on the specific pathways and interactions shown in the knowledge graph."""

            return self._make_api_call(prompt)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _make_api_call(self, prompt: str) -> str:
        """Make OpenAI API call"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # or "gpt-4" if you have access
                messages=[
                    {"role": "system", "content": "You are a medical expert providing accurate, detailed explanations about cancer biology and treatments."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
                
        except Exception as e:
            return f"API Error: {str(e)}"
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
                        color='#666666',
                        arrows='to')
        
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
                
                if info['connected_to']:
                    response += "  Direct relationships:\n"
                    connections = [f"{n['relationship']} {n['entity']}" 
                                 for n in info['connected_to']]
                    response += "   - " + "\n   - ".join(connections) + "\n"
                
                if info['paths']:
                    response += "  Extended relationships:\n"
                    for path in info['paths']:
                        if len(path) > 1:
                            path_str = " → ".join([
                                f"{step['from']} {step['relationship']} {step['to']}"
                                for step in path
                            ])
                            response += f"   - {path_str}\n"
        else:
            response = "No directly relevant information found in the knowledge graph."
            
        return response

def main():
    if not os.getenv("HUGGINGFACE_API_TOKEN"):
        print("Error: Please set the HUGGINGFACE_API_TOKEN environment variable")
        print("\nYou can get your token from: https://huggingface.co/settings/tokens")
        print("\nThen set it using:")
        print("export HUGGINGFACE_API_TOKEN='your_token_here'  # For Unix/Linux/Mac")
        print("set HUGGINGFACE_API_TOKEN=your_token_here  # For Windows")
        return
    
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
    
    print("Initializing systems...")
    try:
        if not os.getenv("HUGGINGFACE_API_TOKEN"):
            raise ValueError("Please set the HUGGINGFACE_API_TOKEN environment variable")
            
        classical_ai = ClassicalAI(cancer_knowledge_base)
        graphrag = GraphRAG()
        
        print("Creating knowledge graph...")
        graphrag.create_knowledge_graph(cancer_knowledge_base)
        
        print("\nGenerating visualization...")
        graph_file = graphrag.visualize_graph()
        print(f"Cancer research knowledge graph visualization saved to: {graph_file}")
        
        print("\nDemo Instructions:")
        print("1. Open 'cancer_research_graph.html' in your web browser to see the interactive visualization")
        print("2. Node colors represent different types:")
        print("   - Green: Drug")
        print("   - Pink: Protein")
        print("   - Blue: Pathway")
        print("   - Orange: Cancer Type")
        print("   - Red: Side Effect")
        print("   - Purple: Gene")
        print("3. Hover over nodes and edges to see additional information")
        print("4. Use the physics button to adjust the graph layout")
        
        test_queries = [
            "Why is Trastuzumab effective for breast cancer?",
            "What are the risks of Trastuzumab treatment?",
            "How does HER2 relate to cancer growth?",
            "Explain the pathway from HER2 to cancer growth",
            "What is the relationship between BRCA1 and cancer risk?",
            "How does the PI3K pathway affect cancer development?"
        ]
        
        print("\nComparing different approaches:")
        for query in test_queries:
            print("\n" + "="*80)
            print(f"Query: {query}")
            
            print("\n1. Basic LLM Response (without knowledge graph):")
            print("-"*40)
            basic_response = classical_ai.raw_query(query)
            print(basic_response)
            
            print("\n2. Knowledge Graph Analysis:")
            print("-"*40)
            graph_response = graphrag.query(query)
            print(graph_response)
            
            print("\n3. Enhanced LLM Response (with knowledge graph context):")
            print("-"*40)
            enhanced_response = classical_ai.query_with_graph_context(query, graph_response)
            print(enhanced_response)
            print("="*80)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nPlease make sure you have:")
        print("1. Set the HUGGINGFACE_API_TOKEN environment variable")
        print("2. Installed all required packages (networkx, pyvis, requests)")
        print("3. Have an active internet connection")

if __name__ == "__main__":
    main()