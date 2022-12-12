class Categoria:
    def __init__(self, id: int, accountId: int, name: str):
        self.id = id
        self.accountId = accountId
        self.name = name

    def __str__(self) -> str:
        return self.name