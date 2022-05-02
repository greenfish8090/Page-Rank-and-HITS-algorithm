# Page-Rank-and-HITS-algorithm
An implementation of the PageRank and HITS algorithms for the course Information Retrieval

[GitHub link](https://github.com/greenfish8090/Page-Rank-and-HITS-algorithm/) <br>
Group members: <br>
Ankita Behera (2019A7PS0075H) <br>
Pranav Balaji (2019A7PS0040H) <br>

## How to use
### Create environment

```
conda env create -f environment.yml
```
### Run PageRank algorithm

```
python page_rank.py --file <filepath> --rtp (true|false)
```
### Run HITS algorithm

```
python hits.py --graph <filepath> --query <term>
```
