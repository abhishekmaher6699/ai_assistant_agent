from memory.models import Memory


class MemoryStore:

    def __init__(self, repository):
        self.repository = repository

    def add(self, key, content, category):
        memory = Memory(
            key=key,
            content=content,
            category=category,
        )

        self.repository.save_memory(memory)

    def get_all(self) -> list[Memory]:
        return self.repository.load_memories()

    def exists(self, content: str) -> bool:
        memories = self.get_all()

        return any(
            memory.content.lower() == content.lower()
            for memory in memories
        )

    def add_extracted(self, memories):
        for item in memories:
            if not isinstance(item, dict):
                continue

            key = item.get("key")
            content = item.get("content")
            category = item.get("category")

            if not key or not content or not category:
                continue

            self.add(key, content, category)