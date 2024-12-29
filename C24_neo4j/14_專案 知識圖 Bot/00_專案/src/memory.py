from typing import Dict, Any, Union, List
from langchain.memory import ConversationKGMemory
from langchain.schema import get_buffer_string


class ConversationEntityKGMemory(ConversationKGMemory):
    """
    Extending ConversationKGMemory providing both chat history
    knowledge of enttiy involved with knowledge graph.
    Supported input key: chat_history_key (default "history") and "entities"
    """

    chat_history_key: str = "history"  #: :meta private:

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        entities = self._get_current_entities(inputs)

        if self.return_messages:
            message_buffer = self.chat_memory.messages[-self.k * 2:]
        else:
            # 原本的腳本會報錯，註解並重寫
            # message_buffer = get_buffer_string(
            #    self.chat_memory.messages[-self.k * 2:],
            #    human_prefix=self.human_prefix,
            #    ai_prefix=self.ai_prefix,
            # )
            # 當 return_messages 為 False 時，取得消息的字串
            buffer_string = get_buffer_string(
                self.chat_memory.messages[-self.k * 2:],
                human_prefix=self.human_prefix,
                ai_prefix=self.ai_prefix,
            )
            # 在 else 情況下為 message_buffer 賦予一個空列表作為傳出使用
            message_buffer = []
            # 這裡暫時不做其他處理，僅輸出
            print(f'=>buffer_string={buffer_string}')

        entity_strings = []
        for entity in entities:
            knowledge = self.kg.get_entity_knowledge(entity)
            if knowledge:
                summary = f"On {entity}: {'. '.join(knowledge)}."
                entity_strings.append(summary)
        entity_info: Union[str, List]
        if not entity_strings:
            entity_info = [] if self.return_messages else ""
        elif self.return_messages:
            entity_info = [
                self.summary_message_cls(content=text) for text in entity_strings
            ]
        else:
            entity_info = "\n".join(entity_strings)

        print(f"Loaded chat history: {message_buffer}")
        print(f"Loaded entity info: {entity_info}")

        return {
            self.chat_history_key: message_buffer,
            "entities": entity_info,
        }

    @property
    def memory_variables(self) -> List[str]:
        """Will always return list of memory variables.

        :meta private:
        """
        return [self.chat_history_key, "entities"]
