from models import Merchant, Client, Transaction
from database import session
from datetime import datetime, timedelta
import random


for i in range(10):
    session.add(Merchant(
        latitude=random.uniform(-90, 90),
        longitude=random.uniform(-180, 180),
        mcc_cd=random.randint(1, 1000)
    ))

for j in range(50):
    session.add(Client(
        gender='Male' if random.random() > 0.5 else 'Female',
        age=random.randint(1, 70)
    ))

for _ in range(500):
    transaction_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 365))
    session.add(Transaction(
        merchant=session.get(Merchant, random.randint(1, 10)),
        client=session.get(Client, random.randint(1, 50)),
        transaction_dttm=transaction_date,
        transaction_amt=round(random.uniform(1, 1000), 2)
    ))

session.commit()
