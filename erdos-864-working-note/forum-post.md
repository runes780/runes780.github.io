I have prepared a short AI-assisted working note related to Erdős Problem #864. This is not a claimed solution and does not improve the known \((\sqrt2+o(1))\sqrt N\) upper bound.

The note isolates a paired-core obstruction. If \(A_0=B\cup(s-B)\), then the relevant lower-side obstruction is

\[
(B+B)\cap(s-D^+(B))=\varnothing.
\]

After normalizing \(B\subseteq[0,L]\), \(0,L\in B\), and writing \(s=3L-\Omega\), this becomes the finite Sidon hole condition

\[
\Omega\notin B+3(L-B).
\]

I define the associated finite extremal function \(g(L,\Omega)\), give small exact branch-and-bound computations, and record a local packing lemma. The computations are only finite evidence and do not prove any asymptotic result. The main missing input appears to be an inverse theorem showing that near-maximal Sidon sets cannot leave holes at positive-density positions in the structured set \(B+3(L-B)\).

I am mainly wondering whether this reformulation, or the finite \(g(L,\Omega)\) subproblem, is already known and whether it is a useful way to isolate the paired-core obstruction.

Working note: https://github.com/runes780/runes780.github.io/blob/master/erdos-864-working-note/working-note.md

Code: https://github.com/runes780/runes780.github.io/blob/master/erdos-864-working-note/erdos864_hole_search.py

Package index: https://github.com/runes780/runes780.github.io/tree/master/erdos-864-working-note

This note was prepared with AI assistance; I have tried to mark clearly what is proved, computed, conjectured, and not claimed.
