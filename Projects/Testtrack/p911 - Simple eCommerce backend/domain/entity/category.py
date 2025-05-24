class Category:
    pass

    def __init__(self, name: str):
        if name == None or name.strip() == None:
            raise ValueError("Category name cannot be empty")
        else:
            self.name = name

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, Category):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"Category(name='{self.name}')"

    def __str__(self):
        return f"{self.name}"

    def get_name(self) -> str:
        return self.name
