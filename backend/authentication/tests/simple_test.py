"""Simple test module."""

from unittest import TestCase


class SimpleTest(TestCase):
    """Class used for ensuring test runner is working, before writing real tests."""

    def test_simple(self):
        """Simple arthemetic test."""
        self.assertEqual(3 + 3, 6)
