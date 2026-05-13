"""seed_cinemas

Revision ID: 5f6b16e71071
Revises: 5f6b16e71070
Create Date: 2026-05-11 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f6b16e71071'
down_revision: Union[str, Sequence[str], None] = '5f6b16e71070'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Данные кинотеатров для инициализации
CINEMAS_DATA = [
    ("Малибу", "г. Липецк, ул. Терешковой, 35б, ТРЦ «Малибу»"),
    ("КИНОМАКС", "г. Липецк, ул. Катукова, 51, ТРЦ «Ривьера»"),
    ("Кинолюкс", "г. Липецк, ул. Титова, 10, ТРЦ «Москва»"),
    ("Остров капитана Флинта", "г. Липецк, ул. Студеновская, 124а, ТРЦ «Липецк»"),
]


def upgrade() -> None:
    """Добавить начальные кинотеатры в таблицу cinemas."""
    cinemas_table = sa.table(
        'cinemas',
        sa.column('name', sa.String),
        sa.column('address', sa.String),
    )
    
    data = [
        {'name': name, 'address': address}
        for name, address in CINEMAS_DATA
    ]
    
    op.bulk_insert(cinemas_table, data)


def downgrade() -> None:
    """Удалить добавленные кинотеатры."""
    op.execute("DELETE FROM cinemas WHERE name IN (%s)" % 
               ', '.join([f"'{name}'" for name, _ in CINEMAS_DATA]))
