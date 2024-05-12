SUFFIX_WITH_ENTITIES = """TOOLS
------
Assistant can ask the user to use tools to look up information that may be helpful in answering the users original question. The tools the human can use are:

{{tools}}

{format_instructions}

USERS IN CONVERSATION
------
Here is a list of users involved in the conversation:
{{{{entities}}}}

USER'S INPUT
--------------------
Here is the user's input (remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else):

{{{{input}}}}"""