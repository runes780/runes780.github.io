# Claim status

<div class="center">

| Status | Item |
|:---|:---|
| Known background | The Erdős–Freud lower-bound construction and the standard $`(\sqrt2+o(1))\sqrt N`$ upper bound. |
| Proved in this note | The deficit equivalence $`(B+B)\cap(s-D^+(B))=\varnothing \iff \Omega\notin B+3(L-B)`$ in the normalized paired-core model, and a local packing inequality. |
| Computed | Exact finite values/examples for selected small $`(L,\Omega)`$ using a branch-and-bound verifier. |
| Conjectured | $`g(L,\Omega)^2\le L-\Omega/3+o(L)`$, as a possible paired-core sub-conjecture. |
| Not claimed | A solution of Erdős #864, a proof of the conjecture, or any unconditional improvement over $`\sqrt2`$. |

</div>

# The original problem

For $`A\subseteq [N]:=\{1,\ldots,N\}`$, define
``` math
r_A(n)=\#\{(a,b):a,b\in A,\ a\le b,\ a+b=n\}.
```
Let
``` math
F(N)=\max\{|A|:A\subseteq [N],\ \#\{n:r_A(n)>1\}\le 1\}.
```
Thus all unordered sums $`a+b`$, $`a\le b`$, are required to be unique
except possibly for one exceptional value.

The lower-bound construction of Erdős and Freud gives
``` math
F(N)\ge \left(\frac{2}{\sqrt3}+o(1)\right)\sqrt N.
```
The question is whether the matching upper bound
``` math
F(N)\le \left(\frac{2}{\sqrt3}+o(1)\right)\sqrt N
```
holds. The standard upper bound currently relevant to this note is
``` math
F(N)\le (\sqrt2+o(1))\sqrt N.
```

# The Erdős–Freud construction

Let $`M=\lfloor N/3\rfloor`$, and choose a Sidon set $`B\subseteq[1,M]`$
with
``` math
|B|=(1+o(1))\sqrt M=(1+o(1))\frac{1}{\sqrt3}\sqrt N.
```
Set
``` math
A=B\cup(N-B),\qquad N-B:=\{N-b:b\in B\}.
```
Since $`B\subseteq[1,N/3]`$, the two parts are disjoint for large $`N`$,
and
``` math
|A|=2|B|=\left(\frac{2}{\sqrt3}+o(1)\right)\sqrt N.
```

Sums inside $`B`$ are unique because $`B`$ is Sidon. Sums inside $`N-B`$
have the form
``` math
(N-b_i)+(N-b_j)=2N-(b_i+b_j),
```
and are also unique. Cross sums have the form
``` math
b_i+(N-b_j)=N+(b_i-b_j).
```
If $`i=j`$, this equals $`N`$, so $`N`$ has $`|B|`$ representations. If
$`i\ne j`$, uniqueness of nonzero ordered differences in a Sidon set
implies the nonexceptional cross sums are unique. The three sum-regions
are interval-separated because $`B\subseteq[1,N/3]`$. Thus $`A`$ has
only one repeated sum, namely $`N`$.

# The $`\sqrt2`$ upper-bound barrier

Suppose $`s`$ is the unique sum with more than one representation.
Splitting $`A`$ around $`s/2`$, the lower and upper pieces are
individually ordinary Sidon sets: any repeated sum entirely on one side
would be different from $`s`$ and hence forbidden. If $`h(M)`$ denotes
the largest Sidon subset of $`[M]`$, then
``` math
|A|\le \max_{0\le t\le N}\{h(t)+h(N-t)\}+o(\sqrt N).
```
Using the classical estimate $`h(M)=\sqrt M+o(\sqrt M)`$ and maximizing
$`\sqrt t+\sqrt{N-t}`$ gives
``` math
F(N)\le(\sqrt2+o(1))\sqrt N.
```
This argument does not use the full structure of the unique exceptional
sum. The rest of this note isolates one piece of that lost structure.

# Paired-core obstruction

Representations of the exceptional sum $`s`$ form a matching, apart from
a possible central loop $`s/2+s/2=s`$. A structured part of $`A`$ may
therefore have the form
``` math
A_0=B\cup(s-B),
```
where $`B`$ is the set of lower endpoints of exceptional pairs.

For such a paired core, the relevant sum families are
``` math
B+B,\qquad s+B-B,\qquad 2s-(B+B).
```
The value $`s`$ itself comes from diagonal cross-pair sums $`b+(s-b)`$.
The lower-side nonexceptional sums below $`s`$ are governed by
``` math
B+B \quad\text{and}\quad s-D^+(B),
```
where
``` math
D^+(B)=\{b_j-b_i:b_i,b_j\in B,\ b_i<b_j\}.
```
Thus the paired-core interlacing condition is
``` math
\label{eq:interlace}
(B+B)\cap(s-D^+(B))=\varnothing.
```
This condition is pointwise. It is not equivalent to interval
separation.

# Deficit formulation

Normalize
``` math
B\subseteq[0,L],\qquad 0,L\in B,
```
and write
``` math
s=3L-\Omega,
\qquad 0<\Omega<L.
```
The range-overlap regime for the paired core is $`2L<s<3L`$, i.e.
$`0<\Omega<L`$. Let
``` math
C=L-B=\{L-b:b\in B\}.
```

<div class="lemma">

**Lemma 1** (Deficit form). *Let $`B\subseteq[0,L]`$ with $`0,L\in B`$,
and let $`s=3L-\Omega`$ with $`0<\Omega<L`$. Then
``` math
(B+B)\cap(s-D^+(B))=\varnothing
```
if and only if
``` math
\Omega\notin B+3(L-B).
```
Equivalently, $`\Omega\notin B+3C`$.*

</div>

<div class="proof">

*Proof.* A collision in
<a href="#eq:interlace" data-reference-type="eqref"
data-reference="eq:interlace">[eq:interlace]</a> has the form
``` math
x+y=s-(z-u),
```
where $`x,y,u,z\in B`$ and $`u<z`$. Equivalently,
``` math
x+y+z-u=s=3L-\Omega.
```
Rearranging gives
``` math
\Omega=u+(L-x)+(L-y)+(L-z),
```
which lies in $`B+3(L-B)`$.

Conversely, suppose
``` math
\Omega=u+(L-x)+(L-y)+(L-z)
```
for some $`u,x,y,z\in B`$. Then
``` math
x+y+z-u=3L-\Omega=s.
```
Because $`0<\Omega<L`$ and all terms in
``` math
u+(L-x)+(L-y)+(L-z)
```
are nonnegative, one must have $`u<z`$; otherwise $`u+(L-z)\ge L`$,
forcing the whole sum to be at least $`L`$. Thus $`z-u\in D^+(B)`$ and
``` math
x+y=s-(z-u),
```
so <a href="#eq:interlace" data-reference-type="eqref"
data-reference="eq:interlace">[eq:interlace]</a> fails. This proves the
equivalence. ◻

</div>

This lemma is the main reduction: the paired-core obstruction is
equivalent to a hole at $`\Omega`$ in the structured fourfold set
$`B+3(L-B)`$.

# The finite extremal function

<div class="definition">

**Definition 1**. *For integers $`L\ge2`$ and $`1\le\Omega\le L-1`$,
define $`g(L,\Omega)`$ to be the largest size of a Sidon set
``` math
B\subseteq[0,L],\qquad 0,L\in B,
```
such that
``` math
\Omega\notin B+3(L-B).
```
*

</div>

The paired-core reduction suggests the following possible asymptotic
sub-conjecture.

<div class="conjecture">

**Conjecture 1** (Sidon hole sub-conjecture). *Uniformly for
$`1\le\Omega\le L-1`$,
``` math
g(L,\Omega)^2\le L-\frac{\Omega}{3}+o(L).
```
Equivalently, if $`\Omega=\eta L`$ with fixed $`0\le\eta\le1`$, then
``` math
g(L,\eta L)\le \left(\sqrt{1-\frac{\eta}{3}}+o(1)\right)\sqrt L.
```
*

</div>

For the pure paired-core model, $`s=3L-\Omega`$. If the conjecture held,
then
``` math
|A_0|=2|B|\le 2\sqrt{L-\Omega/3}+o(\sqrt L)=\frac{2}{\sqrt3}\sqrt s+o(\sqrt s).
```
Thus it would recover the Erdős–Freud constant in the pure paired-core
model. It would not automatically solve the original problem, since
unpaired elements outside the paired core would still require separate
control.

# Exact computation and representative data

The accompanying script `erdos864_hole_search.py` performs exact
branch-and-bound search for $`g(L,\Omega)`$ for small $`L`$. It fixes
$`0,L\in B`$, maintains unordered sums $`B+B`$ including diagonal sums
$`2b`$, maintains positive differences $`D^+(B)`$, and enforces
``` math
(B+B)\cap((3L-\Omega)-D^+(B))=\varnothing.
```
The verifier also checks the equivalent deficit condition
$`\Omega\notin B+3(L-B)`$.

#### How to reproduce.

The code uses only the Python standard library. Basic checks can be run
by
``` math
\texttt{python erdos864\_hole\_search.py --verify-examples}.
```
Selected tables can be regenerated with
``` math
\texttt{python erdos864\_hole\_search.py --exact-ratio-table}.
```
Longer all-$`\Omega`$ scans are available with
``` math
\texttt{python erdos864\_hole\_search.py --all-omega 30}.
```
Increasing the cutoff may become expensive.

<div class="center">

| $`L`$ | $`\Omega`$ | $`g(L,\Omega)`$ | $`g(L,\Omega)/\sqrt L`$ | representative extremal $`B`$ |
|---:|---:|---:|---:|:---|
| 12 | 6 | 5 | 1.443 | $`\{0,1,3,8,12\}`$ |
| 30 | 15 | 7 | 1.278 | $`\{0,1,3,7,12,20,30\}`$ |
| 50 | 49 | 8 | 1.131 | $`\{0,2,5,9,15,23,34,50\}`$ |

</div>

The bare finite inequality $`g(L,\Omega)^2\le L-\Omega/3`$ is often
false for small $`L`$. In the computations, the excess can be several
multiples of $`\sqrt L`$. However, no example in these finite
computations shows an excess clearly of order $`cL`$. This is only
computational evidence; it is not an asymptotic theorem.

## Warning example: range overlap is not pointwise intersection

Let
``` math
B=\{0,1,3,8,12\},\qquad L=12,
\qquad \Omega=6,
```
so $`s=3L-\Omega=30`$. Then
``` math
B+B=\{0,1,2,3,4,6,8,9,11,12,13,15,16,20,24\},
```
and
``` math
D^+(B)=\{1,2,3,4,5,7,8,9,11,12\}.
```
Thus
``` math
30-D^+(B)=\{18,19,21,22,23,25,26,27,28,29\},
```
and hence
``` math
(B+B)\cap(30-D^+(B))=\varnothing.
```
Nevertheless, the ranges overlap on $`[18,24]`$. Any proof that replaces
pointwise disjointness by interval separation would therefore be false.

# A local packing lemma

The following finite lemma is a necessary condition for a hole. It is
useful diagnostically but appears too weak to imply the conjectured
asymptotic bound.

<div class="lemma">

**Lemma 2** (Local deficit packing). *Let $`B\subseteq[0,L]`$, let
$`C=L-B`$, and let $`1\le\Omega\le L-1`$. If
``` math
\Omega\notin B+3C,
```
then
``` math
|(C+C)\cap[0,\Omega]|+|(B+C)\cap[0,\Omega]|\le \Omega+1.
```
*

</div>

<div class="proof">

*Proof.* Since
``` math
B+3C=(B+C)+(C+C),
```
the hypothesis implies
``` math
\Omega\notin(C+C)+(B+C).
```
Equivalently,
``` math
(C+C)\cap(\Omega-(B+C))=\varnothing.
```
Restrict to the interval $`[0,\Omega]`$. The map $`x\mapsto\Omega-x`$ is
a bijection of this interval. Therefore the two subsets
``` math
(C+C)\cap[0,\Omega]
\quad\text{and}\quad
\Omega-((B+C)\cap[0,\Omega])
```
are disjoint subsets of $`[0,\Omega]`$. Their total size is at most
$`\Omega+1`$. ◻

</div>

This lemma is only a first-order local density statement. To prove the
Sidon hole sub-conjecture, one would need inverse information showing
that near-maximal Sidon sets force enough of $`C+C`$ and $`B+C`$ into
the relevant local interval.

# Interpretation and limitations

The reduction above suggests the following missing input:

> If $`B\subseteq[0,L]`$ is a near-maximal Sidon set, then the
> structured fourfold set $`B+3(L-B)`$ cannot have holes at
> positive-density positions $`\Omega`$.

A sharp version would be the Sidon hole sub-conjecture above. At
present, this note provides no proof of such an inverse theorem. It also
does not control unpaired elements in the original Erdős problem.
Therefore the unconditional upper bound remains
``` math
F(N)\le(\sqrt2+o(1))\sqrt N
```
from the methods recalled here.

The main failure points are:

1.  The paired-core condition gives pointwise disjointness, not interval
    separation.

2.  Finite range overlap can be large without producing a collision.

3.  The local packing inequality is necessary but too weak.

4.  The full original problem may contain unpaired elements outside the
    reflected core.

5.  Finite exact computations do not prove asymptotic statements.

Thus the current state is a structural reduction and computational
testbed, not a resolution of Erdős Problem \#864.

# AI assistance disclosure

This note was prepared with AI assistance. The mathematical claims and
computations should be independently checked. No claim is made that
Erdős Problem \#864 is solved. No claim of novelty is made; any result
beyond standard background should be treated as a candidate observation
requiring literature review and independent verification.

# References and context

1.  T. F. Bloom, *Erdős Problem \#864*,
    <https://www.erdosproblems.com/864>. The problem page states the
    open problem, the Erdős–Freud lower bound, and the recommended
    citation format.

2.  Erdős Problems, *Discussion thread for Problem \#864*,
    <https://www.erdosproblems.com/forum/thread/864>. Comments there
    include Desmond Weisenberg’s $`(\sqrt2+o(1))\sqrt N`$ upper-bound
    argument and Terence Tao’s link to finite extremizer data.

3.  GitHub issue \#143 in `teorth/erdosproblems`, *Calculating maximal
    set size for \#864*,
    <https://github.com/teorth/erdosproblems/issues/143>.

4.  Erdős Problems forum rules, <https://www.erdosproblems.com/forum/>.
    These rules request AI disclosure, human checking, and external
    links for long proofs or partial proofs.

5.  `teorth/erdosproblems` wiki, *AI contributions to Erdős problems*,
    <https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems>.
