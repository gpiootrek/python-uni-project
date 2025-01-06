from abc import ABC, abstractmethod
from statistics import mean, median, stdev

class BaseAnalyzer(ABC):
    def __init__(self, results: list):
        """
        results: List of dictionaries containing analysis results.
        """
        self.results = results

    def total_offers(self):
        """Count the total number of job offers."""
        return sum(result["offers_count"] for result in self.results)

    def salary_statistics(self):
        """Calculate descriptive statistics for salaries."""
        salaries_lower = [lower for result in self.results for lower in result["salary_lower_ranges"]]
        salaries_upper = [upper for result in self.results for upper in result["salary_upper_ranges"]]
        
        def calculate_stats(salaries):
            if not salaries:
                return None  # Handle case where no data is present
            return {
                "min": round(min(salaries), 2),
                "max": round(max(salaries), 2),
                "mean": round(mean(salaries), 2),
                "median": round(median(salaries), 2),
                "std_dev": round(stdev(salaries), 2) if len(salaries) > 1 else None,
                "count": len(salaries),
            }

        return {
            "lower_range_stats": calculate_stats(salaries_lower),
            "upper_range_stats": calculate_stats(salaries_upper),
        }

    @abstractmethod
    def analyze(self):
        """Abstract method that must be implemented in derived classes."""
        pass
