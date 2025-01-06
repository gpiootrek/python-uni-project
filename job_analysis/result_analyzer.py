from collections import Counter
from .base_analyzer import BaseAnalyzer

class ResultAnalyzer(BaseAnalyzer):
    def skill_frequency(self):
        """Count the frequency of skills required in the job offers."""
        primary = Counter([req for result in self.results for req in result["primary_requirements"]])
        secondary = Counter([req for result in self.results for req in result["secondary_requirements"]])
        return {"primary": primary, "secondary": secondary}

    def analyze(self):
        """Aggregate analysis results, including total offers, salary statistics, and skill frequency."""
        return {
            "total_offers": self.total_offers(),
            "salary_statistics": self.salary_statistics(),
            "skill_frequency": self.skill_frequency(),
        }
