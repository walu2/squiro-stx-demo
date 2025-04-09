# GDS - Analysis Results

## PageRank 
The PageRank algorithm ranks diseases based on their connectivity within the symptom network. Diseases with higher scores are more central, indicating they tend to be influential hubs that share common, frequently occurring symptoms. This insight helps in identifying key conditions that may play a pivotal role within the overall network.

## Louvain Community Detection
The Louvain algorithm groups diseases into communities by analyzing shared symptom connections. Each community represents a cluster of similar diseases, which facilitates the identification of patterns or common traits that could be further explored for targeted investigations.

## Betweenness Centrality of Symptoms
Betweenness centrality measures how often a symptom lies on the shortest paths between other nodes. Higher scores suggest that the symptom acts as a critical connector, effectively bridging different clusters of diseases and influencing multiple pathways within the network.

## Node Similarities
Node similarity analysis establishes new SIMILAR relationships between diseases based on the overlap in their symptom profiles. A higher similarity score indicates that a pair of diseases shares more symptoms, hinting at a closer clinical relationship that can be useful for clustering and refining diagnostic approaches.

## Conclusion
Each analysis method offers a unique perspective on the disease-symptom network. The PageRank results help identify central conditions, while the Louvain communities reveal clusters of similar diseases. Betweenness centrality emphasizes key connecting symptoms, and node similarity highlights overlapping symptom profiles. Together, these insights can inform further research and improve our understanding of disease interrelations....