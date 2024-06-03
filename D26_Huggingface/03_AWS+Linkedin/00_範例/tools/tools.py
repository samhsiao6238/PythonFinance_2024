from langchain.utilities import SerpAPIWrapper
import requests


class CustomSerpAPIWrapper(SerpAPIWrapper):
    def __init__(self):
        super(CustomSerpAPIWrapper, self).__init__()

    @staticmethod
    def _process_response(res: dict) -> str:
        """Process response from SerpAPI."""
        if "error" in res.keys():
            raise ValueError(f"Got error from SerpAPI: {res['error']}")
        if "organic_results" in res.keys():
            for result in res["organic_results"]:
                if "linkedin.com/in/" in result["link"]:
                    return result["link"]
        return "No good search result found"


def get_profile_url(name: str):
    """搜尋 Linkedin 或 Twitter 個人資料頁面"""
    search = CustomSerpAPIWrapper()
    res = search.run(f"{name} LinkedIn site:linkedin.com")

    # 檢查帶有輸入名稱的直接 URL 是否有效
    direct_url = f"https://tw.linkedin.com/in/{name}"
    response = requests.get(direct_url)
    if response.status_code == 200:
        return direct_url

    return res
