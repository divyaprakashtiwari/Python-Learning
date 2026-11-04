"""
Phase 4 - Topic 09: Abstraction
Example 02: Abstract Properties (`@property` + `@abstractmethod`) & The Template Method Pattern

Demonstrates:
  - Requiring subclasses to implement an abstract `@property` (`driver_name`)
  - Combining concrete orchestration logic (`execute_etl_pipeline()`) in the ABC
    with abstract hook methods (`extract()`, `transform()`) implemented by subclasses
"""

from abc import ABC, abstractmethod


class BaseETLPipeline(ABC):
    """
    Abstract Base Class using the Template Method Pattern:
    `run_pipeline()` is a concrete method on the ABC that orchestrates
    abstract steps (`driver_name`, `extract`, `transform`).
    """

    @property
    @abstractmethod
    def pipeline_name(self) -> str:
        """Subclasses must provide a read-only `pipeline_name` property."""

    @abstractmethod
    def extract_raw(self) -> list[str]:
        """Subclasses must fetch raw records."""

    @abstractmethod
    def transform_record(self, raw: str) -> str:
        """Subclasses must clean/transform a single record."""

    def run_pipeline(self) -> list[str]:
        """Concrete template method shared by all subclasses."""
        raw_items = self.extract_raw()
        cleaned = [self.transform_record(item) for item in raw_items]
        print(f"  [{self.pipeline_name}] Processed {len(cleaned)} records: {cleaned}")
        return cleaned


class UserSignupETL(BaseETLPipeline):
    """Concrete ETL pipeline normalizing user signup emails."""

    @property
    def pipeline_name(self) -> str:
        return "UserSignup-ETL"

    def extract_raw(self) -> list[str]:
        return ["  AARAV@GMAIL.COM ", " Priya@TechCorp.in "]

    def transform_record(self, raw: str) -> str:
        return raw.strip().lower()


def main() -> None:
    print("=== Template Method Pattern with Abstract Properties & Methods ===")
    etl = UserSignupETL()
    etl.run_pipeline()


if __name__ == "__main__":
    main()
