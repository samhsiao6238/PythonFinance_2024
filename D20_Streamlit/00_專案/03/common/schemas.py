from dataclasses import dataclass


@dataclass
class RepositoryData:
    full_name: str
    stars_count: int
    trending_stars_count: int
