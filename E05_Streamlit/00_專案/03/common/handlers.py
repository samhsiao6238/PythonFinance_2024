import re
from dataclasses import asdict
from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional

import requests
from bs4 import BeautifulSoup
from bs4 import Tag

from common.constants import GITHUB_TRENDING_PYTHON_PAGE_URL
from common.constants import GithubTrendingDateRange
from common.schemas import RepositoryData

repo_name_pattern: str = r"([\w\-\_\.]+)"
stars_count_pattern: str = r"([\w\,]+)"


@dataclass
class GithubTrendingHandler:
    """
    A class for retrieving the latest Github trending data for Python language repositories
    by scraping HTML and returning the data as a list of RepositoryData objects or dicts.
    """

    date_range: Optional[GithubTrendingDateRange] = None

    def __get_text_from_strings(self, pattern: str, strings: List[str]) -> List[str]:
        """
        Helper function to extract strings that match a given regular expression pattern.

        Args:
            pattern (str): A regular expression pattern to match against the strings.
            strings (List[str]): A list of strings to search for matches.

        Returns:
            List[str]: A list of strings that match the specified pattern.
        """

        repo_name_parts: List[str] = []

        for input_string in strings:
            if matches := re.search(pattern, input_string):
                extracted_text = matches.group()
                repo_name_parts.append(extracted_text)
        return repo_name_parts

    def __gen_repo_name(self, strings: List[str]) -> str:
        """
        Combine a list of strings into a GitHub repository `full_name`.
        The input list `strings` should have a length of 2.

        Args:
            strings (List[str]): A list of two strings used to create the `full_name`.

        Returns:
            str: The GitHub repository `full_name`.
        """
        if len(strings) != 2:
            return "Unknown"
        return " / ".join(strings)

    def __gen_stars_count(self, strings: List[str]) -> int:
        """
        Convert a list of strings into an integer.

        Example `strings` input: ["1,999"]

        Args:
            strings (List[str]): A list of strings containing numeric values.

        Returns:
            int: The integer representation of the combined numeric values from the strings.
        """
        if len(strings) != 1:
            return 0

        stars_count_str: str = strings[0]
        stars_count_numbers: List[str] = stars_count_str.split(",")

        try:
            return int("".join(stars_count_numbers))
        except ValueError:
            return 0

    def get_repo_full_name(self, repo: Tag) -> str:
        """
        Extract the `full_name` information from a BeautifulSoup Tag.

        Args:
            repo (Tag): A BeautifulSoup Tag object representing the repository information.

        Returns:
            str: The extracted `full_name` as a string.
        """
        repo_name_heading: Optional[Tag] = repo.find("h2", class_="h3 lh-condensed")
        if not repo_name_heading:
            return self.__gen_repo_name(strings=[])

        repo_name_link: Optional[Tag] = repo_name_heading.find("a", class_="Link")
        if not repo_name_link:
            return self.__gen_repo_name(strings=[])

        repo_full_name_strings: List[str] = self.__get_text_from_strings(
            pattern=repo_name_pattern, strings=list(repo_name_link.strings)
        )
        return self.__gen_repo_name(repo_full_name_strings)

    def get_repo_stars_count(self, repo: Tag) -> int:
        """
        Extract the `stars_count` information (as an integer) from a BeautifulSoup Tag.
        The number on the Github page is provided in string format, so it's extracted and converted to an integer.

        Args:
            repo (Tag): A BeautifulSoup Tag object representing the repository information.

        Returns:
            int: The extracted `stars_count` as an integer.
        """
        stars_count_block: Optional[Tag] = repo.find("div", class_="f6 color-fg-muted mt-2")
        if not stars_count_block:
            return self.__gen_stars_count(strings=[])

        stars_count_link: Optional[Tag] = stars_count_block.find("a", class_="Link")
        if not stars_count_link:
            return self.__gen_stars_count(strings=[])

        repo_stars_count_strings: List[str] = self.__get_text_from_strings(
            pattern=stars_count_pattern, strings=list(stars_count_link.strings)
        )
        return self.__gen_stars_count(strings=repo_stars_count_strings)

    def get_repo_trending_stars_count(self, repo: Tag) -> int:
        """
        Extract the `trending_stars_count` information (as an integer) from a BeautifulSoup Tag.
        The number on the Github page is provided in string format, so it's extracted and converted to an integer.

        Args:
            repo (Tag): A BeautifulSoup Tag object representing the repository information.

        Returns:
            int: The extracted `trending_stars_count` as an integer.
        """
        trending_stars_count_block: Optional[Tag] = repo.find("span", class_="d-inline-block float-sm-right")
        if not trending_stars_count_block:
            return self.__gen_stars_count(strings=[])

        trending_stars_count_strings: List[str] = self.__get_text_from_strings(
            pattern=stars_count_pattern,
            strings=list(trending_stars_count_block.strings),
        )
        return self.__gen_stars_count(strings=trending_stars_count_strings)

    def get_repo_data(self, repo: Tag) -> RepositoryData:
        """
        Extract information (`full_name`, `stars_count`, `trending_stars_count`) about a specific repository
        based on a BeautifulSoup Tag.

        Args:
            repo (Tag): A BeautifulSoup Tag object representing the repository information.

        Returns:
            RepositoryData: An object containing the extracted repository data.
        """
        repo_full_name: str = self.get_repo_full_name(repo=repo)
        repo_stars_count: int = self.get_repo_stars_count(repo=repo)
        repo_trending_stars_count: int = self.get_repo_trending_stars_count(repo=repo)

        return RepositoryData(
            full_name=repo_full_name,
            stars_count=repo_stars_count,
            trending_stars_count=repo_trending_stars_count,
        )

    def get_repos(self) -> List[Tag]:
        """
        Get the Github trending Python HTML page while respecting the specified `date_range`.

        Returns:
            List[Tag]: A list of BeautifulSoup Tag objects representing articles (boxes)
            containing information about repositories.
        """
        date_range: GithubTrendingDateRange = self.date_range if self.date_range else GithubTrendingDateRange.weekly
        url = f"{GITHUB_TRENDING_PYTHON_PAGE_URL}?since={date_range.value}"

        page_response: requests.Response = requests.get(url, timeout=10)
        if not page_response.ok:
            raise Exception("Error during loading Github Trending page")

        soup: BeautifulSoup = BeautifulSoup(page_response.content, "html.parser")
        return soup.find_all("article", class_="Box-row")

    def get_repos_data(self) -> List[RepositoryData]:
        """
        Get Github trending Python repositories as a list of RepositoryData objects.

        Returns:
            List[RepositoryData]: A list of RepositoryData objects representing trending repositories.
        """
        repositories: List[Tag] = self.get_repos()

        if not repositories:
            return []

        repos_data: List[RepositoryData] = []
        for repo in repositories:
            repos_data.append(self.get_repo_data(repo=repo))

        return repos_data

    def get_json_repos_data(self) -> List[Dict[str, str]]:
        """
        Get Github trending Python repositories in the following format: List[Dict[str, str]].

        Returns:
            List[Dict[str, str]]: A list of dictionaries representing trending repositories.
            Each dictionary has the following format:
            [{"full_name": "XYZ / 123", "stars_count": "1001", "trending_stars_count": "542"}]
        """
        repos_data: List[RepositoryData] = self.get_repos_data()

        return [asdict(repo_data) for repo_data in repos_data]
