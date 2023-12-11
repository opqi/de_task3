from sqlalchemy import func
from models import AggregatedData
from database import session


total_purchase_2020 = (
    session.query(func.sum(AggregatedData.total_purchase_amount))
    .filter(AggregatedData.transaction_year == 2020)
    .scalar()
)

total_purchase_april_2020 = (
    session.query(func.sum(AggregatedData.total_purchase_amount))
    .filter(AggregatedData.transaction_year == 2020, AggregatedData.transaction_month == 4)
    .scalar()
)

total_purchase_male_2020 = (
    session.query(func.sum(AggregatedData.total_purchase_amount))
    .filter(AggregatedData.gender == 'Male', AggregatedData.transaction_year == 2020)
    .scalar()
)

total_purchase_male_18_31_2020 = (
    session.query(func.sum(AggregatedData.total_purchase_amount))
    .filter(
        AggregatedData.gender == 'Male',
        AggregatedData.age_group == '19-30',
        AggregatedData.transaction_year == 2020
    )
    .scalar()
)

print("Total purchases for all in 2020:", total_purchase_2020)
print("Total purchases for April 2020:", total_purchase_april_2020)
print("Total purchases for all males in 2020:", total_purchase_male_2020)
print("Total purchases for males aged 18-31 in 2020:",
      total_purchase_male_18_31_2020)
