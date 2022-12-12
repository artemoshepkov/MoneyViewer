from contextlib import contextmanager
import sqlite3 as sq
import typing as t

class DB:
    def __init__(self, database_name: str) -> None:
        self.__database_name__ = database_name

    def __connect(self) -> sq.Connection:
        return sq.connect(self.__database_name__)

    @contextmanager
    def __get_cursos(self, connection: sq.Connection) -> sq.Cursor:
        cursor = connection.cursor()

        # yield cursor

        try:
            yield cursor
        except sq.OperationalError:
            print(sq.OperationalError)
            connection.rollback()
        except:
            print("Something wrong with DB command!")
            connection.rollback()
        else:
            connection.commit()

    def execute(self, sql_command: str, params: t.Optional[t.Tuple[t.Any]] = ()):
        with self.__get_cursos(self.__connect()) as cursor:
            return cursor.execute(sql_command, params)



    # def get_transactions(self) -> list[t.Any]:
    #     command = """SELECT * FROM transact;"""

    #     return self.db.execute(command)

    # def add_transaction(self, transaction: str) -> None:
    #     command = """INSERT INTO transact ()"""

    #     self.db.execute(command)

    # def get_accounts(self) -> list[t.Any]:
    #     command = """SELECT * FROM acount;"""

    #     return self.db.execute(command)

    # def add_account(self, account_name: str) -> None:
    #     command = """INSERT INTO acount (name) VALUES(%s)"""

    #     self.db.execute(command, ("name", account_name))


# CREATE TABLE account(
#     id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
#     name VARCHAR(50) NOT NULL
#     );

# CREATE TABLE type_transaction(
#     id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
#     name VARCHAR(50) NOT NULL
#     );

# CREATE TABLE goal(
#     id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
#   	account_id INT NOT NULL,
#   	name VARCHAR(50) NOT NULL,
#   	money_amount DOUBLE NOT NULL,
#   	finish_money_amount DOUBLE NOT NULL,
#   	FOREIGN KEY (account_id) REFERENCES account(id)
#     );

# CREATE TABLE transact(
#     id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
#   	account_id INT NOT NULL,
#   	type_id INT NOT NULL,
#   	name VARCHAR(50) NOT NULL,
#   	date DATE NOT NULL,
#   	payment DOUBLE NOT NULL,
#   	FOREIGN KEY (account_id) REFERENCES account(id),
#   	FOREIGN KEY (type_id) REFERENCES type_transaction(id)
#     );