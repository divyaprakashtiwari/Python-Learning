"""
Topic 08 - Modules and Packages: Question 7
Problem: Itertools Analytical Stream Engine (count, cycle, islice, chain, accumulate, compress, product, combinations).
"""

import itertools
from typing import Any, Dict, List, Tuple


class ItertoolsDataEngine:
    """Orchestrates itertools combinatorics, generator streams, and running aggregations."""

    def generate_interleaved_events(self, batch_count: int, initial_seq: int = 1000) -> List[Dict[str, Any]]:
        """Harvests bounded events combining infinite count() and cycle() via islice()."""
        seq_stream = itertools.count(start=initial_seq)
        worker_cycle = itertools.cycle(["NODE_ALPHA", "NODE_BETA", "NODE_GAMMA"])
        paired_stream = zip(seq_stream, worker_cycle)

        # Safely slice infinite generator to bounded batch_count
        sliced = itertools.islice(paired_stream, batch_count)
        return [{"seq": s, "worker": w} for s, w in sliced]

    def merge_and_track_running_total(self, stream_east: List[float], stream_west: List[float]) -> List[float]:
        """Chains multiple streams and computes cumulative running prefix totals."""
        chained = itertools.chain(stream_east, stream_west)
        return list(itertools.accumulate(chained))

    def filter_by_health_mask(self, servers: List[str], health_mask: List[bool]) -> List[str]:
        """Applies parallel boolean filtering using itertools.compress."""
        return list(itertools.compress(servers, health_mask))

    def build_hyperparameter_grid(
        self,
        learning_rates: List[float],
        batch_sizes: List[int],
        optimizers: List[str]
    ) -> List[Dict[str, Any]]:
        """Generates Cartesian product parameter combinations."""
        return [
            {"lr": lr, "batch": b, "opt": opt}
            for lr, b, opt in itertools.product(learning_rates, batch_sizes, optimizers)
        ]

    def generate_tournament_pairs(self, teams: List[str]) -> List[Tuple[str, str]]:
        """Generates all unique 2-element tournament pairings without order repetition."""
        return list(itertools.combinations(teams, 2))


# Verification & Execution
engine = ItertoolsDataEngine()

stream_events = engine.generate_interleaved_events(batch_count=4, initial_seq=5001)
print(f"Interleaved Events ({len(stream_events)} items):")
for idx, evt in enumerate(stream_events, 1):
    print(f"{idx}. Seq: {evt['seq']} | Worker: {evt['worker']}")

running_totals = engine.merge_and_track_running_total([100.0, 50.0], [25.0, 75.0])
print(f"\nMerged Running Totals: {running_totals}")

healthy_nodes = engine.filter_by_health_mask(["srv-1", "srv-2", "srv-3", "srv-4"], [True, False, True, False])
print(f"Filtered Healthy Nodes: {healthy_nodes}")

grid = engine.build_hyperparameter_grid([0.01, 0.1], [32, 64], ["adam"])
print(f"Hyperparameter Grid ({len(grid)} combinations):")
print(f"{grid[:2]} ...")

pairings = engine.generate_tournament_pairs(["Red", "Blue", "Green"])
print(f"Tournament Pairings ({len(pairings)} unique matches): {pairings}")
