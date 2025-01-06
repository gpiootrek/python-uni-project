import unittest
from job_analysis.base_analyzer import BaseAnalyzer
from statistics import mean, median, stdev

# A simple subclass of BaseAnalyzer for testing
class TestAnalyzer(BaseAnalyzer):
    def analyze(self):
        """Since BaseAnalyzer is abstract, we provide a dummy implementation."""
        return {}

class TestBaseAnalyzer(unittest.TestCase):
    def setUp(self):
        self.results = [
            {
                "offers_count": 5,
                "salary_lower_ranges": [3000, 4000, 5000],
                "salary_upper_ranges": [7000, 8000, 9000],
                "primary_requirements": ["Python", "SQL"],
                "secondary_requirements": ["AWS", "Docker"],
            }
        ]
        # Use TestAnalyzer to avoid the abstract method error
        self.analyzer = TestAnalyzer(self.results)

    def test_total_offers(self):
        """Test total offers calculation."""
        expected_total = 5
        self.assertEqual(self.analyzer.total_offers(), expected_total)

    def test_salary_statistics(self):
        """Test salary statistics calculation."""
        salary_stats = self.analyzer.salary_statistics()

        # Lower salary range statistics (3000, 4000, 5000)
        lower_range_stats = salary_stats["lower_range_stats"]
        self.assertEqual(lower_range_stats["min"], 3000)
        self.assertEqual(lower_range_stats["max"], 5000)
        self.assertEqual(lower_range_stats["mean"], mean([3000, 4000, 5000]))
        self.assertEqual(lower_range_stats["median"], median([3000, 4000, 5000]))
        self.assertEqual(lower_range_stats["std_dev"], round(stdev([3000, 4000, 5000]), 2))
        self.assertEqual(lower_range_stats["count"], 3)

        # Upper salary range statistics (7000, 8000, 9000)
        upper_range_stats = salary_stats["upper_range_stats"]
        self.assertEqual(upper_range_stats["min"], 7000)
        self.assertEqual(upper_range_stats["max"], 9000)
        self.assertEqual(upper_range_stats["mean"], mean([7000, 8000, 9000]))
        self.assertEqual(upper_range_stats["median"], median([7000, 8000, 9000]))
        self.assertEqual(upper_range_stats["std_dev"], round(stdev([7000, 8000, 9000]), 2))
        self.assertEqual(upper_range_stats["count"], 3)
