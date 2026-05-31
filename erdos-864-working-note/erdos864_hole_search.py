#!/usr/bin/env python3
"""
Exact and diagnostic search code for the finite Sidon hole problem associated
with Erdős Problem #864.

Given L and Omega, define g(L,Omega) to be the largest size of a Sidon set
B subset [0,L] with 0,L in B and Omega not in B + 3(L-B).  Equivalently,
with s = 3L - Omega, require
    (B+B) cap (s - D^+(B)) = empty.

This script uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import random
from math import sqrt
from typing import Iterable, Optional, Sequence, Tuple


def sumset_unordered(B: Sequence[int]) -> set[int]:
    """Return B+B using unordered pairs i <= j, including diagonal sums."""
    B = tuple(sorted(B))
    return {B[i] + B[j] for i in range(len(B)) for j in range(i, len(B))}


def diffset_plus(B: Sequence[int]) -> set[int]:
    """Return D^+(B) = {b_j - b_i : i < j}."""
    B = tuple(sorted(B))
    return {B[j] - B[i] for i in range(len(B)) for j in range(i + 1, len(B))}


def is_sidon(B: Sequence[int]) -> bool:
    """Check the ordinary unordered Sidon condition."""
    B = tuple(sorted(B))
    return len(sumset_unordered(B)) == len(B) * (len(B) + 1) // 2


def hole_ok_original(B: Sequence[int], L: int, Omega: int) -> bool:
    """Check (B+B) cap ((3L-Omega)-D^+(B)) = empty."""
    s = 3 * L - Omega
    S = sumset_unordered(B)
    D = diffset_plus(B)
    return all((s - d) not in S for d in D)


def hole_ok_deficit(B: Sequence[int], L: int, Omega: int) -> bool:
    """Check Omega not in B + 3(L-B), allowing repetitions in 3(L-B)."""
    B = tuple(sorted(B))
    C = [L - b for b in B]
    c3 = {c1 + c2 + c3 for c1 in C for c2 in C for c3 in C}
    return all((Omega - b) not in c3 for b in B)


def verify_B(B: Sequence[int], L: int, Omega: int, verbose: bool = False) -> bool:
    """Independent verifier for a candidate feasible set B."""
    B = tuple(sorted(B))
    ok_endpoints = bool(B) and B[0] == 0 and B[-1] == L
    ok_range = all(0 <= b <= L for b in B)
    ok_distinct = len(B) == len(set(B))
    ok_sidon = is_sidon(B)
    ok_hole_original = hole_ok_original(B, L, Omega)
    ok_hole_deficit = hole_ok_deficit(B, L, Omega)
    ok = ok_endpoints and ok_range and ok_distinct and ok_sidon and ok_hole_original and ok_hole_deficit

    if verbose:
        s = 3 * L - Omega
        print(f"B = {B}")
        print(f"L = {L}, Omega = {Omega}, s = {s}")
        print(f"endpoints: {ok_endpoints}")
        print(f"range: {ok_range}")
        print(f"distinct: {ok_distinct}")
        print(f"Sidon: {ok_sidon}")
        print(f"hole original: {ok_hole_original}")
        print(f"hole deficit: {ok_hole_deficit}")
        S = sumset_unordered(B)
        D = diffset_plus(B)
        comp = {s - d for d in D}
        print(f"B+B = {sorted(S)}")
        print(f"D^+(B) = {sorted(D)}")
        print(f"s-D^+(B) = {sorted(comp)}")
        print(f"intersection = {sorted(S & comp)}")

    return ok


def ratio_to_omega(L: int, eta: float) -> int:
    """Convert a target ratio eta to an integer Omega in [1,L-1]."""
    if eta <= 0:
        return 1
    return max(1, min(L - 1, int(round(eta * L))))


def diff_capacity_bound(L: int) -> int:
    """Largest t satisfying binom(t,2) <= L."""
    t = int((1 + sqrt(1 + 8 * L)) // 2)
    while t * (t - 1) // 2 > L:
        t -= 1
    while (t + 1) * t // 2 <= L:
        t += 1
    return t


def exact_g(
    L: int,
    Omega: int,
    store_limit: int = 3,
    seed_examples: Optional[Iterable[Sequence[int]]] = None,
) -> tuple[int, list[tuple[int, ...]], int]:
    """Exact computation of g(L,Omega) by branch-and-bound."""
    if L < 2:
        raise ValueError("Need L >= 2")
    if not (1 <= Omega <= L - 1):
        raise ValueError("Need 1 <= Omega <= L-1")

    s = 3 * L - Omega
    B = [0, L]

    sums_mask = (1 << 0) | (1 << L) | (1 << (2 * L))
    diffs_mask = 1 << L
    compD_mask = 0
    q = s - L
    if 0 <= q <= 2 * L:
        compD_mask |= 1 << q

    best = 2
    best_examples: list[tuple[int, ...]] = [(0, L)] if store_limit else []
    nodes = 0
    max_by_diff = diff_capacity_bound(L)

    if seed_examples:
        for ex in seed_examples:
            ex = tuple(sorted(ex))
            if verify_B(ex, L, Omega):
                if len(ex) > best:
                    best = len(ex)
                    best_examples = [ex] if store_limit else []
                elif len(ex) == best and store_limit and len(best_examples) < store_limit and ex not in best_examples:
                    best_examples.append(ex)

    def make_masks_for_add(x: int):
        nonlocal sums_mask, diffs_mask, compD_mask
        sm = 0
        for y in B:
            bit = 1 << (x + y)
            if sm & bit:
                return None
            sm |= bit
        bit = 1 << (2 * x)
        if sm & bit:
            return None
        sm |= bit
        if sm & sums_mask:
            return None

        dm = 0
        cm = 0
        for y in B:
            d = abs(x - y)
            bit = 1 << d
            if dm & bit:
                return None
            dm |= bit
            q = s - d
            if 0 <= q <= 2 * L:
                cm |= 1 << q
        if dm & diffs_mask:
            return None
        if (sums_mask | sm) & (compD_mask | cm):
            return None
        return sm, dm, cm

    def record_current():
        nonlocal best, best_examples
        m = len(B)
        ex = tuple(sorted(B))
        if m > best:
            best = m
            best_examples = [ex] if store_limit else []
        elif m == best and store_limit and len(best_examples) < store_limit and ex not in best_examples:
            best_examples.append(ex)

    def dfs(remaining: tuple[int, ...]):
        nonlocal sums_mask, diffs_mask, compD_mask, nodes
        nodes += 1
        m = len(B)
        if m + len(remaining) < best:
            return
        if min(m + len(remaining), max_by_diff) < best:
            return

        feasible = []
        info = []
        for x in remaining:
            masks = make_masks_for_add(x)
            if masks is not None:
                feasible.append(x)
                info.append(masks)

        if m + len(feasible) < best:
            return
        if min(m + len(feasible), max_by_diff) < best:
            return

        record_current()
        n = len(feasible)
        for idx, x in enumerate(feasible):
            if m + 1 + (n - idx - 1) < best:
                break
            sm, dm, cm = info[idx]
            B.append(x)
            sums_mask |= sm
            diffs_mask |= dm
            compD_mask |= cm
            dfs(tuple(feasible[idx + 1 :]))
            compD_mask &= ~cm
            diffs_mask &= ~dm
            sums_mask &= ~sm
            B.pop()

    dfs(tuple(range(1, L)))
    return best, best_examples, nodes


def greedy_feasible_set(L: int, Omega: int, seed: int = 0, order: str = "random") -> tuple[int, ...]:
    """Greedy construction of a feasible B. This is not exact."""
    rng = random.Random(seed)
    s = 3 * L - Omega
    B = [0, L]
    sums_mask = (1 << 0) | (1 << L) | (1 << (2 * L))
    diffs_mask = 1 << L
    compD_mask = 0
    q = s - L
    if 0 <= q <= 2 * L:
        compD_mask |= 1 << q

    candidates = list(range(1, L))
    if order == "random":
        rng.shuffle(candidates)
    elif order == "middle":
        candidates.sort(key=lambda x: (abs(x - L / 2), rng.random()))
    elif order == "ends":
        candidates.sort(key=lambda x: (min(x, L - x), rng.random()))

    def candidate_masks(x: int):
        nonlocal sums_mask, diffs_mask, compD_mask
        sm = 0
        for y in B:
            bit = 1 << (x + y)
            if sm & bit:
                return None
            sm |= bit
        bit = 1 << (2 * x)
        if sm & bit:
            return None
        sm |= bit
        if sm & sums_mask:
            return None
        dm = 0
        cm = 0
        for y in B:
            d = abs(x - y)
            bit = 1 << d
            if dm & bit:
                return None
            dm |= bit
            q = s - d
            if 0 <= q <= 2 * L:
                cm |= 1 << q
        if dm & diffs_mask:
            return None
        if (sums_mask | sm) & (compD_mask | cm):
            return None
        return sm, dm, cm

    for x in candidates:
        masks = candidate_masks(x)
        if masks is None:
            continue
        sm, dm, cm = masks
        B.append(x)
        sums_mask |= sm
        diffs_mask |= dm
        compD_mask |= cm
    return tuple(sorted(B))


def print_exact_ratio_table(L_values=(10, 12, 20, 30, 40, 50), etas=(0, 0.25, 0.5, 0.75, 0.9, 0.98)):
    print("| L | eta target | Omega used | g | g/sqrt(L) | predicted coeff | excess/sqrt(L) | example |")
    print("|---:|---:|---:|---:|---:|---:|---:|---|")
    for L in L_values:
        for eta in etas:
            Omega = ratio_to_omega(L, eta)
            g, examples, nodes = exact_g(L, Omega, store_limit=1)
            pred = sqrt(1 - Omega / (3 * L))
            excess = (g * g - (L - Omega / 3)) / sqrt(L)
            print(f"| {L} | {eta:g} | {Omega} | {g} | {g / sqrt(L):.3f} | {pred:.3f} | {excess:.2f} | `{examples[0]}` |")


def print_exact_all_omega_summary(Lmax: int = 30):
    print("| L | Omega searched | max g | #Omega attaining max g | Omega of max excess | g there | max excess/sqrt(L) | example |")
    print("|---:|---:|---:|---:|---:|---:|---:|---|")
    for L in range(2, Lmax + 1):
        vals = []
        for Omega in range(1, L):
            g, examples, nodes = exact_g(L, Omega, store_limit=1)
            vals.append((Omega, g, examples[0]))
        max_g = max(g for _, g, _ in vals)
        num_max = sum(1 for _, g, _ in vals if g == max_g)
        best_excess = None
        for Omega, g, example in vals:
            excess = (g * g - (L - Omega / 3)) / sqrt(L)
            record = (excess, Omega, g, example)
            if best_excess is None or record > best_excess:
                best_excess = record
        excess, Omega_star, g_star, example_star = best_excess
        print(f"| {L} | 1..{L-1} | {max_g} | {num_max} | {Omega_star} | {g_star} | {excess:.2f} | `{example_star}` |")


def verify_examples() -> None:
    examples = [
        ((0, 1, 3, 8, 12), 12, 6),
        ((0, 1, 3, 7, 12, 20, 30), 30, 15),
        ((0, 2, 5, 9, 15, 23, 34, 50), 50, 49),
    ]
    for B, L, Omega in examples:
        print("-" * 60)
        assert verify_B(B, L, Omega, verbose=True)
    print("All representative examples verified.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Search for finite Sidon hole examples g(L,Omega).")
    parser.add_argument("--verify-examples", action="store_true", help="Verify representative examples from the note.")
    parser.add_argument("--exact", nargs=2, metavar=("L", "OMEGA"), type=int, help="Compute exact g(L,Omega).")
    parser.add_argument("--exact-ratio-table", action="store_true", help="Print selected exact ratio table.")
    parser.add_argument("--all-omega", type=int, metavar="LMAX", help="Print all-Omega summary for L <= LMAX.")
    args = parser.parse_args()

    if args.verify_examples:
        verify_examples()
    if args.exact:
        L, Omega = args.exact
        g, examples, nodes = exact_g(L, Omega, store_limit=5)
        print(f"g({L},{Omega}) = {g}; nodes = {nodes}")
        for ex in examples:
            print(ex)
    if args.exact_ratio_table:
        print_exact_ratio_table()
    if args.all_omega is not None:
        print_exact_all_omega_summary(args.all_omega)
    if not any([args.verify_examples, args.exact, args.exact_ratio_table, args.all_omega is not None]):
        parser.print_help()


if __name__ == "__main__":
    main()
