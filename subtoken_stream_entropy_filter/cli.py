"""CLI for subtoken-stream-entropy-filter."""
import sys
import argparse
from .filter import SubtokenStreamEntropyFilter


def main():
    parser = argparse.ArgumentParser(description="Subtoken Stream Entropy Filter CLI")
    parser.add_argument("--demo", action="store_true", help="Run token entropy filter demo")
    args = parser.parse_args()

    if args.demo:
        filt = SubtokenStreamEntropyFilter(window_size=5, min_entropy=0.5)
        loop_tokens = ["repeat", "repeat", "repeat", "repeat", "repeat", "repeat"]
        print("[*] Feeding degenerate repetitive stream:")
        for t in loop_tokens:
            res = filt.feed_token(t)
            print(f"    Token '{t}' -> Entropy: {res['entropy']:.2f} | Verdict: {res['verdict']} | Halt={res['should_halt']}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
