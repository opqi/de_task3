from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, declared_attr, declarative_base

Base = declarative_base()

class Merchant(Base):
    __tablename__ = 'merchants'
    merchant_id = Column(Integer, primary_key=True)
    latitude = Column(DECIMAL(8, 6))
    longitude = Column(DECIMAL(9, 6))
    mcc_cd = Column(Integer)

    @declared_attr
    def transactions(cls):
        return relationship('Transaction', back_populates='merchant')

    def __init__(self, latitude, longitude, mcc_cd):
        self.latitude = latitude
        self.longitude = longitude
        self.mcc_cd = mcc_cd

class Client(Base):
    __tablename__ = 'clients'
    client_id = Column(Integer, primary_key=True)
    gender = Column(String(10))
    age = Column(Integer)

    @declared_attr
    def transactions(cls):
        return relationship('Transaction', back_populates='client')

    def __init__(self, gender, age):
        self.gender = gender
        self.age = age

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

    def __init__(self, gender, age_group, mcc_cd, transaction_year, transaction_month,
                 total_purchase_amount, average_purchase_amount, total_transactions_count):
        self.gender = gender
        self.age_group = age_group
        self.mcc_cd = mcc_cd
        self.transaction_year = transaction_year
        self.transaction_month = transaction_month
        self.total_purchase_amount = total_purchase_amount
        self.average_purchase_amount = average_purchase_amount
        self.total_transactions_count = total_transactions_count
