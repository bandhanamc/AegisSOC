from app.ai.core.service_manager import AIServiceManager

a = AIServiceManager()

b = AIServiceManager()

print(a is b)

print(type(a.matcher))

print(type(a.search))

print(type(a.llm))

print(type(a.knowledge))

print(type(a.memory))