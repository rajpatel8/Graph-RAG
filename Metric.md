# Evaluation Metrics Scoring Methodology

Our scoring system (0-5) is based on specific criteria for each metric, designed to measure the quality and completeness of responses:

## 1. Relationship Depth (0-5)
- **5**: Complete multi-hop relationships identified with all intermediate connections
- **4**: Multiple relationship levels with most intermediate connections
- **3**: Direct relationships with some extended connections
- **2**: Only direct relationships identified
- **1**: Partial or incorrect relationships
- **0**: No relationships identified

Example: For the query "How does HER2 relate to cancer growth?"
- Basic LLM (2.33): Only mentioned HER2 regulates cell growth
- GraphRAG (4.66): Showed complete pathway (HER2 → ERBB2 → PI3K → Cell Growth → Cancer)

## 2. Pathway Completeness (0-5)
- **5**: Full biological pathway with all intermediate steps
- **4**: Most pathway steps with clear connections
- **3**: Basic pathway with some key steps
- **2**: Incomplete pathway with gaps
- **1**: Only start/end points identified
- **0**: No pathway information

Example: For Trastuzumab mechanism
- Basic LLM (1.67): Only mentioned "targets HER2"
- GraphRAG (4.34): Showed complete chain (Trastuzumab → HER2 → Cell Growth → Cancer)

## 3. Clinical Relevance (0-5)
- **5**: Complete clinical implications with mechanisms and effects
- **4**: Clear clinical relevance with most implications
- **3**: Basic clinical implications identified
- **2**: Limited clinical context
- **1**: Minimal clinical relevance
- **0**: No clinical information

Example: For side effects query
- Basic LLM (2.67): Mentioned cardiotoxicity without context
- GraphRAG (4.67): Explained mechanism, monitoring needs, and clinical management

## 4. Mechanism Clarity (0-5)
- **5**: Clear, detailed mechanism with all steps explained
- **4**: Mostly clear mechanism with key steps
- **3**: Basic mechanism with some details
- **2**: Unclear or incomplete mechanism
- **1**: Confusing or incorrect mechanism
- **0**: No mechanism explained

Example: For drug action query
- Basic LLM (2.67): Simple "drug targets protein" explanation
- GraphRAG (4.34): Detailed molecular pathway with biological context

## Scoring Process
Scores are calculated by:
1. Evaluating responses against predefined criteria
2. Averaging multiple evaluators' scores
3. Cross-referencing with known medical knowledge
4. Validating through structured knowledge graph paths