class Goal:
    def __init__(self, id: int, accountId: int, name: str, moneyAmount: float, finishMoneyAmount: float):
        self.id = id
        self.accountId = accountId
        self.name = name
        self.moneyAmount = moneyAmount
        self.finishMoneyAmount = finishMoneyAmount

    def __str__(self) -> str:
        return self.name + "\t" + str(self.moneyAmount)+ "\t" + str(self.finishMoneyAmount) 
