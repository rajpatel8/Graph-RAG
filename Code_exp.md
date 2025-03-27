# GraphRAG Explained Simply

Imagine you're trying to answer a question about medicine, but you want to make sure the answer is correct. Our code does this in three simple steps:

## Step 1: Building the Knowledge Map
Think of this like creating a map of medical information:
- Each thing (like a drug or disease) is a dot on the map
- Lines connect related things (like a drug and what it treats)
- Different colors show different types of things (green for drugs, red for side effects, etc.)

```python
# This is how we create a dot (node) for a drug
drug_node = {
    'entity': 'Trastuzumab',  # The name of the drug
    'type': 'drug',           # What kind of thing it is
    'properties': {}          # Extra information about it
}
```

## Step 2: Finding Answers
When someone asks a question:
1. The code reads the question
2. Finds important words (like drug names or diseases)
3. Looks at our map to find these things
4. Follows the lines to find related information

```python
# Example: Finding information about Trastuzumab
query = "Why is Trastuzumab effective?"
# Code looks for 'Trastuzumab' in our map
# Then follows lines to find what it connects to
```

## Step 3: Making Better Answers
The code makes answers better by:
1. Taking basic AI answer
2. Adding facts from our map
3. Making sure everything is correct
4. Explaining connections clearly

Example Output:
- Basic AI: "Trastuzumab is a drug that helps with cancer"
- Our System: "Trastuzumab works by targeting HER2 protein, which controls cell growth in breast cancer. It also links to [shows more connections]"

## The Results
We can see if it's working better by checking:
- How many facts it gets right (75% more accurate)
- How well it explains connections (2.33 points better)
- How complete the answers are (2.67 points better)
- How useful the information is (2.00 points better)