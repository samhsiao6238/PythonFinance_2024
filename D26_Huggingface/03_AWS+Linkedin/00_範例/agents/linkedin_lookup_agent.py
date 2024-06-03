from tools.tools import get_profile_url
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms.bedrock import Bedrock
from langchain.agents import initialize_agent, Tool, AgentType


def get_llm():
    bedrock_llm = Bedrock(
        model_id="anthropic.claude-v2",
        model_kwargs={
            "temperature": 0.1,
            "max_tokens_to_sample": 4096
        }
    )
    return bedrock_llm


# 搜尋，使用一個佔位符 `name_of_person`
def lookup(name: str) -> str:
    load_dotenv()
    # 建立模板字串
    template = """
    請使用全名 {name_of_person} LinkedIn 進行搜尋，給我一個指向這個人的 LinkedIn 個人資料頁面的連結。
    你的答案必須僅包含 LinkedIn 個人資料的 URL。
    """

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url,
            description="useful for when you need get the LinkedIn Page URL",
        ),
    ]
    # 建立 LLM 物件
    llm = get_llm()
    # 建立 langchain.agents 物件
    agent_chain = initialize_agent(
        tools_for_agent,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    # 建立模板對象，使用模板字串 `template`
    prompt_template = PromptTemplate(
        input_variables=["name_of_person"],
        template=template
    )

    # 取的 LLM 的輸出
    try:
        # 透過 angchain.agents 物件執行 LLM
        linkedin_username = agent_chain.run(
            handle_parsing_errors=True,
            # 輸入
            input=prompt_template.format_prompt(
                name_of_person=f"{name} LinkedIn"
            )
        )
    except ValueError as e:
        print("解析 LLM 發生錯誤：", e)
        return None

    return linkedin_username
