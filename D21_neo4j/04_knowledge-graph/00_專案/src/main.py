# main.py
from neo4j_langchain_bot import Neo4jLangchainBot


def main():
    chatbot = Neo4jLangchainBot()
    while True:
        message = input("You: ")
        response = chatbot.chat_completion(message)
        print("Chatbot: ", response)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interrupt, quitting")
        pass
