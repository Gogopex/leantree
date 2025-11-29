"""
tests:
- start process pool, request server (with Mathlib import), return server, request again and measure
  that the second request does not take longer than a few milliseconds
"""