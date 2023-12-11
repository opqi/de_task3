from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, TIMESTAMP, func, extract, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import random

Base = declarative_base()

class Merchant(Base):
    __tablename__ = 'merchants'
    merchant_id = Column(Integer, primary_key=True)
    latitude = Column(DECIMAL(8, 6))
    longitude = Column(DECIMAL(9, 6))
    mcc_cd = Column(Integer)

class Client(Base):
    __tablename__ = 'clients'
    client_id = Column(Integer, primary_key=True)
    gender = Column(String(10))
    age = Column(Integer)

class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True)
    merchant_id = Column(Integer, ForeignKey('merchants.merchant_id'))
    client_id = Column(Integer, ForeignKey('clients.client_id'))
    transaction_dttm = Column(TIMESTAMP)
    transaction_amt = Column(DECIMAL(10, 2))
    
    merchant = relationship('Merchant', back_populates='transactions')
    client = relationship('Client', back_populates='transactions')

class AggregatedData(Base):
    __tablename__ = 'aggregated_data'
    id = Column(Integer, primary_key=True)
    gender = Column(String(10))
    age_group = Column(String(20))
    mcc_cd = Column(Integer)
    transaction_year = Column(Integer)
    transaction_month = Column(Integer)
    total_purchase_amount = Column(DECIMAL(15, 2))
    average_purchase_amount = Column(DECIMAL(15, 2))
    total_transactions_count = Column(Integer)

# Установка связей между таблицами
Merchant.transactions = relationship('Transaction', back_populates='merchant')
Client.transactions = relationship('Transaction', back_populates='client')

# Создание соединения с базой данных
engine = create_engine('postgresql://your_username:your_password@localhost/your_database')

# Создание таблиц
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Генерация тестовых данных
for _ in range(500):
    session.add(Transaction(
        merchant=session.query(Merchant).get(random.randint(1, 10)),
        client=session.query(Client).get(random.randint(1, 50)),
        transaction_dttm=datetime.utcnow(),
        transaction_amt=round(random.uniform(1, 1000), 2)
    ))

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

# Сохранение данных в базу данных
session.commit()

# Запрос для расчета агрегатов
result = (
    session.query(
        func.sum(Transaction.transaction_amt).label('total_purchase_amount'),
        func.avg(Transaction.transaction_amt).label('average_purchase_amount'),
        func.count().label('total_transactions_count'),
        Client.gender,
        func.CASE(
            [
                (Client.age <= 18, 'Under 18'),
                (Client.age.between(19, 30), '19-30'),
            ],
            else_='31 and older'
        ).label('age_group'),
        Merchant.mcc_cd,
        extract('year', Transaction.transaction_dttm).label('transaction_year'),
        extract('month', Transaction.transaction_dttm).label('transaction_month')
    )
    .join(Merchant)
    .join(Client)
    .group_by(Client.gender, 'age_group', Merchant.mcc_cd, 'transaction_year', 'transaction_month')
    .all()
)

# Заполнение таблицы aggregated_data
for row in result:
    session.add(AggregatedData(
        gender=row.gender,
        age_group=row.age_group,
        mcc_cd=row.mcc_cd,
        transaction_year=row.transaction_year,
        transaction_month=row.transaction_month,
        total_purchase_amount=row.total_purchase_amount,
        average_purchase_amount=row.average_purchase_amount,
        total_transactions_count=row.total_transactions_count
    ))

# Сохранение данных в базу данных
session.commit()

# Примеры запросов к aggregated_data
# Сумма вообще всех покупок за 2020 год
total_purchase_2020 = (
    session.query(func.sum(AggregatedData.total_purchase_amount))
    .filter(AggregatedData.transaction_year == 2020)
    .scalar()
)

# Сумма всех покупок за апрель 2020 года
total_purchase_april_2020 = (
    session.query(func.sum(AggregatedData.total_purchase_amount))
    .filter(AggregatedData.transaction_year == 2020, AggregatedData.transaction_month == 4)
    .scalar()
)

# Сумма покупок всех мужчин за 2020 год
total_purchase_male_2020 = (
    session.query(func.sum(AggregatedData.total_purchase_amount))
    .filter(AggregatedData.gender == 'Male', AggregatedData.transaction_year == 2020)
    .scalar()
)

# Сумма покупок всех мужчин в возрасте 18-31 за 2020 год
total_purchase_male_18_31_2020 = (
    session.query(func.sum(AggregatedData.total_purchase_amount))
    .filter(
        AggregatedData.gender == 'Male',
        AggregatedData.age_group == '19-30',
        AggregatedData.transaction_year == 2020
    )
    .scalar()
)

print("Сумма вообще всех покупок за 2020 год:", total_purchase_2020)
print("Сумма всех покупок за апрель 2020 года:", total_purchase_april_2020)
print("Сумма покупок всех мужчин за 2020 год:", total_purchase_male_2020)
print("Сумма покупок всех мужчин в возрасте 18-31 за 2020 год:", total_purchase_male_18_31_2020)
