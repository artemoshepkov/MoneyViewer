from datetime import date

class Transaction:
    def __init__(self, id: int,accountId: int, categoriaId: int, registDate: date, payment: float) -> None:
        self.id = id
        self.accountId = accountId
        self.registDate = registDate
        self.payment = payment
        self.categoriaId = categoriaId

    def __str__(self):
        return str(self.payment)