# Page-Rank-and-HITS-algorithm
An implementation of the PageRank and HITS algorithms for the course Information Retrieval

[GitHub link](https://github.com/greenfish8090/Page-Rank-and-HITS-algorithm/) <br>
Group members: <br>
Ankita Behera (2019A7PS0075H) <br>
Pranav Balaji (2019A7PS0040H) <br>

## How to use
### Create environment

```
$ conda env create -f environment.yml
```
### Run PageRank algorithm

```
$ python page_rank.py --file <filepath> --rtp (true|false)
```
**Example**
```
$ python page_rank.py --file input2.txt --rtp 0.1
```
**Output**
```
Steady state calculated using left eigen decomposition:
[0.0843 0.0438 0.0957 0.0615 0.0748 0.1476 0.1816 0.0985 0.1144 0.0979]
Steady state calculated using power iteration:
[0.0843 0.0438 0.0957 0.0615 0.0748 0.1476 0.1816 0.0985 0.1144 0.0979]
Converged in 91 steps
```

### Run HITS algorithm

```
$ python hits.py --graph <filepath> --query <term>
```
**Example**
```
$ python hits.py --graph web_graph.gpickle --query war
```
**Output**
```
Hub scores:
[-0.      0.1488  0.     -0.     -0.     -0.     -0.     -0.     -0.
  0.2654  0.     -0.     -0.      0.      0.117  -0.      0.0469 -0.
  0.119   0.191   0.0743 -0.     -0.      0.0375 -0.      0.     -0.
 -0.     -0.     -0.     -0.     -0.    ]
Authority scores:
[0.0989 0.     0.     0.     0.2134 0.1601 0.     0.     0.     0.
 0.     0.     0.     0.     0.     0.1511 0.     0.     0.     0.
 0.     0.2445 0.     0.     0.     0.     0.     0.     0.     0.
 0.1319 0.    ]
 ```
