"""Core Subtoken Stream Entropy Filter implementation."""
import math
from collections import Counter
from typing import List, Dict, Optional, Any


class StreamVerdict:
    NORMAL = "NORMAL"
    REPETITIVE_DEGENERATION = "REPETITIVE_DEGENERATION"
    HIGH_ENTROPY_CHAOS = "HIGH_ENTROPY_CHAOS"


class SubtokenStreamEntropyFilter:
    def __init__(self, window_size: int = 15, min_entropy: float = 1.0, max_entropy: float = 5.0):
        self.window_size = window_size
        self.min_entropy = min_entropy
        self.max_entropy = max_entropy
        self.buffer: List[str] = []

    def compute_entropy(self, tokens: List[str]) -> float:
        if not tokens:
            return 0.0
        counts = Counter(tokens)
        total = float(len(tokens))
        entropy = 0.0
        for count in counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    def feed_token(self, token: str) -> Dict[str, Any]:
        self.buffer.append(token)
        if len(self.buffer) > self.window_size:
            self.buffer.pop(0)

        if len(self.buffer) < self.window_size:
            return {"verdict": StreamVerdict.NORMAL, "entropy": 0.0, "should_halt": False}

        h = self.compute_entropy(self.buffer)
        if h < self.min_entropy:
            return {"verdict": StreamVerdict.REPETITIVE_DEGENERATION, "entropy": h, "should_halt": True}
        if h > self.max_entropy:
            return {"verdict": StreamVerdict.HIGH_ENTROPY_CHAOS, "entropy": h, "should_halt": True}

        return {"verdict": StreamVerdict.NORMAL, "entropy": h, "should_halt": False}
