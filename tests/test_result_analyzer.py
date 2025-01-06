import unittest
from job_analysis.result_analyzer import ResultAnalyzer

class TestResultAnalyzer(unittest.TestCase):
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
        self.analyzer = ResultAnalyzer(self.results)

    def test_skill_frequency_primary(self):
        """Test that skill frequencies for primary requirements are calculated correctly."""
        skill_frequency = self.analyzer.skill_frequency()
        primary_freq = skill_frequency["primary"]

        # Check that 'Python' appears once and 'SQL' once
        self.assertEqual(primary_freq["Python"], 1)
        self.assertEqual(primary_freq["SQL"], 1)

    def test_skill_frequency_secondary(self):
        """Test that skill frequencies for secondary requirements are calculated correctly."""
        skill_frequency = self.analyzer.skill_frequency()
        secondary_freq = skill_frequency["secondary"]

        # Check that 'AWS' appears once and 'Docker' once
        self.assertEqual(secondary_freq["AWS"], 1)
        self.assertEqual(secondary_freq["Docker"], 1)

    def test_analyze(self):
        """Test the analyze method to ensure it returns non-empty results."""
        analysis_results = self.analyzer.analyze()
        # Check that the analysis results are not empty
        self.assertIsNotNone(analysis_results)
        self.assertGreater(len(analysis_results), 0)  # Check if the result is not empty