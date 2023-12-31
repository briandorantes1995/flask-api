"""First

Revision ID: 612fc570a068
Revises: 
Create Date: 2023-11-11 02:18:10.217513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '612fc570a068'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('empleado',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('rol', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    mysql_engine='InnoDB'
    )
    op.create_table('tipo_habitacion',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tipo', sa.String(length=255), nullable=True),
    sa.Column('descripcion', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tipo'),
    mysql_engine='InnoDB'
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('hospedado', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    mysql_engine='InnoDB'
    )
    op.create_table('habitaciones',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('numero', sa.String(length=255), nullable=False),
    sa.Column('costo', sa.String(length=255), nullable=False),
    sa.Column('tipo_habitacion_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tipo_habitacion_id'], ['tipo_habitacion.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_table('reservacion',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('reservado_desde', sa.DateTime(), nullable=True),
    sa.Column('dias', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.Column('habitacion_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['habitacion_id'], ['habitaciones.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservacion')
    op.drop_table('habitaciones')
    op.drop_table('usuario')
    op.drop_table('tipo_habitacion')
    op.drop_table('empleado')
    # ### end Alembic commands ###
