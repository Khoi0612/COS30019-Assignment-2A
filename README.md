# Path-Finding
A Python-based project to visualize and benchmark various path-finding algorithms on randomly generated graphs. Includes both command-line and GUI support.

---

## 📁 Files

| Filename                     | Description                                                                         |
| ---------------------------- | ----------------------------------------------------------------------------------- |
| `path_finding_algorithms.py` | Contains the implementation and execution logic for all supported search algorithms |
| `random_path_generator.py`   | Generates random graphs for testing and optionally visualizes them                  |
| `graph_gui.py`               | GUI component that draws graphs and displays algorithm results                      |
| `utils.py`                   | Utility functions used across the codebase                                          |

---

## ▶ How to Run

### 1. Generate Random Graphs

```bash
py random_path_generator.py {i} -d
```

#### Arguments:

* `i`: Number of graphs to generate
* `-d`: (Optional) Include this flag to draw the graph as it's generated

#### Example:

```bash
py random_path_generator.py 3 -d   # Generates and draws 3 graphs
py random_path_generator.py 5      # Generates 5 graphs silently
```

---

### 2. Run Search Algorithms

```bash
py path_finding_algorithms.py test_{i}.txt {algorithms}
```

#### Arguments:

* `i`: Graph number (e.g. `1`, `2`, `3`, ...) or `-a` to run on **all** graph files
* `algorithms`: Any of the following (case-sensitive):

  * `DFS` – Depth First Search
  * `BFS` – Breadth First Search
  * `GBFS` – Greedy Best First Search
  * `AS` – A\* Search
  * `CUS1`, `CUS2` – Custom algorithms (user-defined)
  * `-a` – Run **all algorithms** on the selected file(s)

#### Examples:

```bash
py path_finding_algorithms.py test_1.txt DFS BFS     # Run DFS and BFS on test_1.txt
py path_finding_algorithms.py test_2.txt -a          # Run all algorithms on test_2.txt
py path_finding_algorithms.py -a -a                  # Run all algorithms on all test files
```

---

## 🧠 Supported Algorithms

* ✅ Depth First Search (DFS)
* ✅ Breadth First Search (BFS)
* ✅ Greedy Best First Search (GBFS)
* ✅ A\* Search (AS)
* ✅ Custom Algorithm 1 (CUS1)
* ✅ Custom Algorithm 2 (CUS2)
