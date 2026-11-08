"""Unit tests for subtoken-stream-entropy-filter."""
import unittest
from subtoken_stream_entropy_filter.filter import SubtokenStreamEntropyFilter, StreamVerdict


class TestSubtokenStreamEntropyFilter(unittest.TestCase):
    def test_repetitive_loop_detected(self):
        f = SubtokenStreamEntropyFilter(window_size=4, min_entropy=0.2)
        for _ in range(3):
            res = f.feed_token("loop")
            self.assertFalse(res["should_halt"])
        # Fourth identical token triggers window check
        res = f.feed_token("loop")
        self.assertTrue(res["should_halt"])
        self.assertEqual(res["verdict"], StreamVerdict.REPETITIVE_DEGENERATION)

    def test_normal_diverse_stream(self):
        f = SubtokenStreamEntropyFilter(window_size=4, min_entropy=0.5)
        tokens = ["apple", "banana", "cherry", "date"]
        for t in tokens:
            res = f.feed_token(t)
        self.assertFalse(res["should_halt"])
        self.assertEqual(res["verdict"], StreamVerdict.NORMAL)
