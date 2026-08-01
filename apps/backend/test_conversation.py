from app.ai.memory.conversation import Conversation

chat = Conversation()

chat.user("Explain SQL Injection")

chat.assistant("SQL Injection explanation")

chat.user("Generate Sigma")

print(chat.history())