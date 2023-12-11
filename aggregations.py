from sqlalchemy import func, extract, case
from models import Transaction, Merchant, Client, AggregatedData
from database import session


result = (
    session.query(
        func.sum(Transaction.transaction_amt).label('total_purchase_amount'),
        func.avg(Transaction.transaction_amt).label('average_purchase_amount'),
        func.count().label('total_transactions_count'),
        Client.gender,
        case(
            (Client.age <= 18, 'Under 18'),
            (Client.age.between(19, 30), '19-30'),
            else_='31 and older'
        ).label('age_group'),
        Merchant.mcc_cd,
        extract('year', Transaction.transaction_dttm).label(
            'transaction_year'),
        extract('month', Transaction.transaction_dttm).label(
            'transaction_month')
    )
    .join(Merchant)
    .join(Client)
    .group_by(Client.gender, 'age_group', Merchant.mcc_cd, 'transaction_year', 'transaction_month')
    .all()
)

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

session.commit()
