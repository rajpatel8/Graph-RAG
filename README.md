# GraphRAG: Enhanced LLM Accuracy through Knowledge Graphs

This project demonstrates an innovative approach to improving Large Language Model (LLM) responses by integrating dynamic knowledge graphs. The implementation shows particular effectiveness in medical domain applications, specifically in cancer research knowledge representation.

## Team Members

| Name | Institution | Email |
|------|-------------|--------|
| Chandravallika Murarisetty | University of Windsor | murarisc@uwindsor.ca |
| Devang Parmar | University of Windsor | parmar1c@uwindsor.ca |
| Preshna Patel | University of Windsor | patel3ab@uwindsor.ca |
| Pranav Shrivastava | University of Windsor | shriva51@uwindsor.ca |
| RajKumar Patel | University of Windsor | patel9qb@uwindsor.ca |
| Vansh Patel | University of Windsor | patel3hb@uwindsor.ca |

## Overview

GraphRAG combines traditional LLM capabilities with structured knowledge representation through graphs, providing:
- Enhanced accuracy in domain-specific queries
- Reduced hallucinations in LLM responses
- Clear visualization of knowledge relationships
- Improved reasoning capabilities

## Features

- Interactive knowledge graph visualization
- Multiple response comparison
- Path-based relationship analysis
- Dynamic knowledge integration
- Color-coded entity categorization

## Technical Stack

- NetworkX for graph operations
- PyVis for interactive visualization
- OpenAI/Hugging Face API integration
- Python 3.x

## Installation

```bash
# Clone the repository
git clone https://github.com/rajpatel8/Graph-RAG
cd Graph-RAG

# Install required packages
pip install networkx pyvis requests openai
```

## Configuration

Set up your API keys:
```bash
# For OpenAI API
export OPENAI_API_KEY='your_openai_key'

# For Hugging Face API
export HUGGINGFACE_API_TOKEN='your_huggingface_token'
```

## Usage

The project includes several versions demonstrating different aspects:

1. Basic Implementation (v0.1.py):
   - Simple knowledge graph construction
   - Basic visualization

2. Classical vs GraphRAG Comparison (v0.2.py):
   - Template-based responses
   - Graph-based responses

3. Medical Domain Implementation (v0.3.py):
   - Cancer research knowledge base
   - Enhanced relationship tracking

4. LLM Integration (v1.0.py onwards):
   - API integration
   - Enhanced response generation

To run the demo:
```bash
python v1.4.py  # Latest version
```

## Example Output

The system provides three types of responses for each query:
1. Basic LLM response
2. Knowledge Graph Analysis
3. Enhanced LLM response with graph context

Example visualization is saved as 'cancer_research_graph.html'.

## Results

Our implementation shows significant improvements:
- Relationship Depth: +2.33 points
- Pathway Completeness: +2.67 points
- Clinical Relevance: +2.00 points
- 75% reduction in hallucinations

## Project Structure

```
.
├── README.md
├── v0.1.py         # Basic implementation
├── v0.2.py         # Comparison implementation
├── v0.3.py         # Medical domain
├── v1.0.py         # Initial LLM integration
├── v1.1.py         # Enhanced error handling
├── v1.3.py         # Multiple response types
└── v1.4.py         # Final implementation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this code in your research, please cite:
```
@misc{graphrag2025,
  author = {Murarisetty, C. and Parmar, D. and Patel, P. and Shrivastava, P. and Patel, R. and Patel, V.},
  title = {GraphRAG: Enhanced LLM Accuracy through Knowledge Graphs},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/rajpatel8/Graph-RAG}}
}
```

## Acknowledgments

- Advanced Database Topics course at University of Windsor
- Dr. Shafaq Khan for project supervision

©2025 Summer (Dr. Shafaq Khan) Advanced Database Topics, All rights reserved.
