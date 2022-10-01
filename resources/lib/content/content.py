"""A base dataclass module with common properties and methods for movies and shows."""

from dataclasses import asdict, dataclass


@dataclass
class Content:
    """Class to build information about movies."""

    file: str
    title: str
    type: str
    status: str
    year: int

    def __str__(self):
        """Return str title formatted with file path."""
        return f"[B]{self.title}[/B] - [I]{self.file}[/I]"

    @property
    def formed_title(self) -> str:
        """Return title formatted with formed_title.

        Returns:
            str: title (year)
        """
        return f"{self.title} {self.formed_year}"

    @property
    def formed_year(self) -> str:
        """Return year inside parentheses.
        Returns:
            str: (year)
        """
        return f"({self.year})"

    @property
    def asdict(self) -> dict:
        """Return a dict from dataclass.
        Returns:
            dict: dict with dataclass properties.
        """
        return asdict(self)
