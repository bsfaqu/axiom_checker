# axiom_checker
Command line utilities to check, generate, and explore directed transit functions and step systems.

# Installation

Make sure to have a python 3.x installation with networkx installed. The networkx package can be installed with the following command:

```pip install networkx```

# Usage

The general workflow of the check.py tool of axiom_checker is to first generate a .tsv file template with ```make_tsv.py``` that allows you to define your transit function,
and then to supply this file to ```check.py``` for axiom checking. In the following we outline how to use these individual scripts.

## make_csv.py

This script creates a tsv file for a chosen number of vertices. Call it with

```python make_tsv.py [vertices] [filename]```

### Directed Transit Functions

For example, creating an empty .tsv for a transit function on V={u,v,w} and saving it to example.tsv can be done with:
```python make_tsv.py u,v,w example.tsv```

The script then outputs the following table which is also saved to ```example.tsv```:
```
        u       v       w
u       *       *       *
v       *       *       *
w       *       *       *
```

You can then use a text editor or spreadsheet editor of your choice to alter the transit function table.
The rows of the .tsv are the first "argument" of the transit function, and the columns are the second
"argument" of the transit function. Consider the following .tsv:


```
        u       v       w
u       *       u,v,w   u,w
v               *       
w               w,v     *
```
The transit function it describes is defined on V={u,v,w} where R(u,w)={u,w}, R(w,v)={w,v}, R(u,v)={u,w,v},
R(u,u)={u}, R(w,w)={w}, R(v,v)={u}, and the transit function of every other pair of vertices is the empty set.

Note that the "Ü" in the u,u/v,v/w,w colums defaults to the transit set that is given by (t0).

Furthermore, any other field that is filled with "*" will default to include the transit set that corresponds to the shortest paths in G_R. If no such path exists in G_R, the transit function of this pair is set to the empty set. Take care that fields contains no character (no space) for transit sets that are supposed to be empty to avoid them being defaulted to the vertices of shortest paths in G_R.

For an example of utilizing "*" in the different fields, replacing the field that corresponds to R(u,v) with "*", and all the empty fields with "*", will yield the same transit function for the example above:


```
        u       v       w
u       *       *       u,w
v       *       *       *
w       *       w,v     *
```

### Signpost Systems

If we take the example from above, created with ```python make_tsv.py u,v,w example.tsv``` we can also use the generated .tsv to describe a signpost system.

For the signpost system, each value in a field corresponds to a triple ([row], [value], [column]). For example, the (proper) signpost system for a P_3 can be described by the following .tsv:

```
        u       v       w
u       *       v       v
v       u       *       w
w       v       v       *
```

The signpost system that this .tsv describes is {(u, v, v), (u, v, w), (v, u, u), (v, w, w), (w, v, v), (w, v, u)}.

Similarly as for directed transit functions, the "*" character is used as a placeholder for triples that should be derived from G_S. The same P_3 as above can be obtained with the following .tsv:

```
        u       v       w
u       *       v       *
v       *       *       w
w       *       *       *
```

## check.py

This script reads a supplied .tsv file and checks it for a selected set of axioms. 
Call it with 

```python check.py --axioms [axioms] --filename [filename]```.

OR

```python check.py -a [axioms] -f [filename]```.

For example, checking the exampe above for axioms (b1), (b3), and (tr2) can be achieved by the following command:

```python check.py -a b1,b3,tr2 -f example.tsv```.

Take note that the axioms supplied as the second argument have to be separated by "," and cannot include spaces.

If you want to check signpost systems, just include a --signpost/-s flag, e.g., ```python check.py --signpost A,G,H example.tsv``` to check whether the step system described in example.tsv satisfies (A), (G), and (H) axioms.


### Directed Transit Functions

The axioms that are supported as of now for directed transit functions are exactly the axioms that appear in the manuscript "Directed Interval Transit Functions" [link to manuscript will be included once published].
The possible axiom strings to supply to ```check.py``` are:


| Axiom in manuscript    | check.py alias |
| -------- | ------- |
| (t0)  | t0    |
| (t1) | t1 (checked by default) |
| (t2s)    | t2s    |
| (t2a)    | t2s    |
| (t3)    | t3 (checked by default)   |
| (tr2)    | tr2    |
| (b1_1)    | b1    |
| (b1_2)    | b1    |
| (b2)    | b2   |
| (b3_1)    | b3    |
| (b3_2)    | b3    |
| (b4)    | b4    |
| (b6_1)    | b6    |
| (b6_2)    | b6    |
| (b6_3)    | b6    |
| (j2)    | j2   |
| (F)    | F    |
| (G)    | G    |
| (co0)    | co0    |
| (co1)    | co1    |
| (co2)    | co2    |
| (co3)    | co3    |
| (g)    | g    |
| (p)    | p    |
| (Mod)    | Mod    |
| (Med)    | Med    |
| (b5)    | b5    |
| graphic    | graphic    |


### Signpost Systems

The axioms that are supported as of now for signpost systems are the axioms that appear in the manuscript "Step Systems of Ptolemaic Graphs" [link to manuscript will be included once published].
The possible axiom strings to supply to ```check.py``` are:

| Axiom in manuscript    | check.py alias |
| -------- | ------- |
| (A)  | A    |
| (B)  | B    |
| (H)  | H    |
| (C)  | C    |
| (D)  | D    |
| (F)  | F    |
| (G)  | G    |
| (E)  | E    |
| (B)  | B    |
| (Dd)  | Dd    |
| (Dt)  | Dt    |
| (Cw)  | Cw    |
| (Cb)  | Cb    |
| (Dm)  | Dm    |
| (T1)  | T1    |
| (T2)  | T2    |
| (Tb2)  | Tb2    |
| (P4)  | P4    |
| (Sm)  | Sm    |
| graphic  | graphic    |

Besides outputting violations of the chosen axioms, and validating if the stepsystem of G_S is equal to S, ```axiom_checker``` also constructs the graph G_S and saves it as a figure. The figure of G_S is saved under the same name as the supplied .tsv, but with a .png file extention.

## explore.py

```explore.py``` is a python command line utility to generate examples of directed transit functions and signpost systems that satisfy a given set of axioms, and violate another set of given axioms. The axioms supported are the same axioms that are available for ```check.py```.

```explore.py``` supports multiple modes. Please include the ```--signpost``` if you want to check signpost systems.

For every mode, the ```-s/--satisfies [axioms]``` or ```-v/--violates [axioms]``` flags have to be included.
For every mode, explore ensures that the generated exampels satisfy the ```-s [axioms]``` and violate the ```-v [axioms]```.

```-s/--satisfies``` and ```-v/--violates``` have to be followed with a comma separated axiom string, e.g. 'b1,b5,tr2'.

In case no axioms are required to be satisfied/violated, just an 'X' can be supplied, e.g. -s X or -v X.

Take note that 'graphic' can also be included as an axiom, for which is then checked if R_{G_R} = R for directed transit functions, and the analogue for signpost systems.


### Iterate all undirected graphs <= 7 vertices:


This can be done with:
```python explore.py [--signpost] --satisfies [axioms] --violates [axioms].```

OR

```python explore.py [--signpost] -s [axioms] -v [axioms].```

The ```--signpost``` flag is optional, hence should be used if you want to explore signpost systems.

Optional arguments include:


```-n [integer] / --nodes [integer]``` - For a minimum number of vertices.


```-o [directory] / --output [directory]``` - To write .png/.tsv of the generated examples to the directory.


```--connected``` - To filter for connected graphs


```--2connected``` - To filter for two-connected graphs


```--contains [directory]``` - To filter for graphs containing induced subgraphs.
                         There should be .tsv files with transit functions/signpost systems that
                         contain these induced subgraphs. File format should be the same as required for
                         check.py. Can also be the output directory from another explore.py call.

                         
```--free [directory]```     - To filter for graphs NOT containing induced subgraphs.
                         There should be .tsv files with transit functions/signpost systems that
                         describe these forbidden subgraphs. File format should be the same as required for
                         check.py. Can also be the output directory from another explore.py call.


### Generate random graphs (undirected for --signpost, directed for DTF)

This can be done with:
```python explore.py [--signpost] --satisfies [axioms] --violates [axioms] --randomgraph [num_tries] --nodes [num_nodes] --probabilities [probabilitylist].```

OR

```python explore.py [--signpost] -s [axioms] -v [axioms] -rg [num_tries] -n [num_nodes] -p [probabilitylist].```

The [probabilitylist] should be a comma-separated list of edge-probabilities. Make sure to not include any spaces in this string. For example, ```-p 0.1,0.2,0.3,0.9``` is a valid probability string.

The ```--signpost flag``` is optional, hence should be used if you want to explore signpost systems.

For example
```explore.py -s [sat_axioms] -v [viol_axioms] -rg 100 -n 5 -p 0.1,0.3,0.7 -o examples/```

Randomly generates 100 graphs of 5 vertices with edge probability 10%, ...,  100 graphs of 5 vertices with edge probability 70% and checks for each of them if they satisfy the axioms [sat_axioms] and violate the [viol_axioms]. Graphs that satisfy [sat_axioms] and violate [viol_axioms] are saved to the examples/ directory in .tsv format (and their visualization as .png).

Optional arguments include:

```-o [directory] / --output [directory]``` - To write .png (figure) and .tsv of the generated examples to the directory.

```--connected``` - To filter for connected graphs

```--2connected``` - To filter for two-connected graphs

```--contains [directory]``` - To filter for graphs containing induced subgraphs.
                         There should be .tsv files with transit functions/signpost systems that
                         contain these induced subgraphs. File format should be the same as required for
                         check.py. Can also be the output directory from another explore.py call.
                         
```--free [directory]```     - To filter for graphs NOT containing induced subgraphs.
                         There should be .tsv files with transit functions/signpost systems that
                         describe these forbidden subgraphs. File format should be the same as required for
                         check.py. Can also be the output directory from another explore.py call.


### Generate random functions

This can be done with:
```python explore.py [--signpost] --satisfies [axioms] --violates [axioms] --randomfunction [num_tries] --nodes [num_nodes] --probabilities [probabilitylist].```

OR

```python explore.py [--signpost] -s [axioms] -v [axioms] -rf [num_tries] -n [num_nodes] -p [probabilitylist].```

The [probabilitylist] should be a comma-separated list of edge-probabilities. Make sure to not include any spaces in this string. For example, ```-p 0.1,0.2,0.3,0.9``` is a valid probability string.

The ```--signpost``` flag is optional, hence should be used if you want to explore signpost systems.

For example,
```explore.py -s [sat_axioms] -v [viol_axioms] -rf 100 -n 5 -p 0.1,0.3,0.7 -o examples/```

Randomly generates 100 directed transit functions on 5 vertices with the 'inclusion-probability 10%', ..., 100 directed transit functions on 5 vertices with the 'inclusion-probability 70%'. Inclusion probability here conceptually is that for every R(u,v), all remaining vertices are included in R(u,v) with P(x in R(u,v))=0.1/0.3/0.7. The method for randomly creating these always ensures that u,v in R(u,v) if R(u,v) is not empty. Similarly it ensures that u in R(u, u).

For signpost systems, the set of all possiple triples on [num_vertices] is computed and then 10%/.../70% of these tuples are randomly selected and the signpost system is checked for the axioms.

Optional arguments include:

```-o [directory] / --output [directory]``` - To write .png (figure) and .tsv of the generated examples to the directory.

---

```axiom_checker``` is licensed under CC BY-SA 4.0.




