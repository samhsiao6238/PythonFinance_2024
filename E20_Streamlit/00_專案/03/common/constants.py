from enum import Enum

GITHUB_TRENDING_PYTHON_PAGE_URL = "https://github.com/trending/python"


class GithubTrendingDateRange(Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
