# Erdős #864 paired-core working note

This directory contains an AI-assisted working note and verification code for a small finite computation related to Erdős Problem #864.

Important caveats:

- This is not a claimed solution of Erdős Problem #864.
- This does not improve the unconditional `(sqrt(2)+o(1))sqrt(N)` upper bound.
- The computations are finite evidence only.
- The note was prepared with AI assistance and should be independently checked.

Files:

- [working-note.md](working-note.md) — forum-facing working note in Markdown.
- [erdos864_hole_search.py](erdos864_hole_search.py) — standard-library Python verifier and exact branch-and-bound search for `g(L, Omega)`.
- [forum-post.md](forum-post.md) — short forum comment draft with public links.

Suggested verification commands:

```bash
python3 erdos864_hole_search.py --verify-examples
python3 erdos864_hole_search.py --exact 12 6
python3 erdos864_hole_search.py --exact-ratio-table
```
