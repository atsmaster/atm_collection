from client.model.CoinEntry import CoinEntry
from db.Database import Database


def print_hi(name):
    database = Database().conn()
    database.create_tables([CoinEntry])
    aa=0


if __name__ == '__main__':
    print_hi('PyCharm')

