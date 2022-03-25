# Repository content

This folder contains the code for the project *Auditing Wikipedia’s Hyperlinks Network on Polarizing Topics*. We execute the code on a 42 core machine.

# Execution pipeline:

Unless specified, all the following scripts are executed in this folder. Before running the script be sure it has the following organization.
- `wiki/`
    | `scripts.py`
    | - `data/`
        | -  `dumps/`
            | - `batches/`
            | - `clickstreams/`
        | -  `graphs/`
        | -  `partitions/`
        | -  `wikipedia_all/`
        | -  `wikipedia_batches/`
        | -  `adj_matrix/`
        | -  `models/`

1. Create a `to_download.txt` file that gathers the links to dumps we want to download.
2. Run `bash downloader.sh to_download.txt` inside the folder `data/dumps/batches/`
3. Run `python feature_extraction_parallel.py --lang <LANG>`, `LANG` is the language you want to parse: en, de, it.
4. Now we concatenate the files we got. We move to `data/wikipedia_batches/`, concatenate all the file containing the same information `cat $(ls | grep _len_text_articles) > len_text_articles.txt.bz2`. Eventually move them to the folder: `data/wikipedia_all/`.
5. [__OPTIONAL__] This passege is not mandatory. In facts, if you already have the list of nodes for each partition of the topic you skip it. `python graph_nodes.py`. For using this script you need to substitute the value of `if_R` and `if_B` with the list of categories you find in the files `TOPIC_categories.txt` (where the first dictionary corresponds to R and the second to B).
    - The list of articles we used for each topics are in `data/partitions/` thus you __do not__ need to execute `python graph_nodes.py`
    - In `graph_nodes.py`, under the name of `categories_dict` you find the seed categories for each topic. The final sets of categories for each topics are in `TOPIC_categories.txt` files.
6. Get the redirections and substitutes titles with ids. `python index_redirection.py`.
7. Get the edges of entire Wikipedia (keeping only ns=0 articles and solving redirections) - save links position. `python index_graph.py`
8. Create the file `click_to_download.txt` which contains the urls of all the clickstream data you want to download.
9. Run `bash downloader.sh click_to_download.txt` inside the folder `data/dumps/clickstreams/`
19. Get for each edge the clickstream over a period (sum up) `python clickstream_extraction.py --lang <LANG>`, `LANG` is the language you want to parse: en, de, it.
11. Give the topic get the induced network. `python read_edges.py --topic <TOPIC>`, where TOPIC is the topic's name.
12. Clicks and edges for green to super node. `python get_info_neigh.py`.
13. Clicks and edges for green to super node. `python position_info.py`.
14. Run `python compute_graph_info.py --topic <TOPIC>` get statistics on the graph
15. Run `python compute_search_through_rate.py --topic <TOPIC>` get click through for clickstrea kind of graph
16. Rum `python AdjMatrix.py --topic <TOPIC>` that computes for each graph its adjacency matrix
17. Run `python models_kdd.py --topic <TOPIC> --sample 150`
18. Notebook Models




# Useful commands
1. `grep "^765$(printf '\t')" adj_lists.txt` get the adj list searching the article by id.
2. `grep "$(printf '\t')abortion$" id_titles.txt` look for the index of an article.
