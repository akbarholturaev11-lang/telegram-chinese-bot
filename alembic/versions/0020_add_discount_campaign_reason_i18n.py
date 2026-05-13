"""add discount campaign reason i18n

Revision ID: 0020_add_discount_campaign_reason_i18n
Revises: 0019_add_discount_campaign_title_i18n
Create Date: 2026-05-13
"""

from alembic import op
import sqlalchemy as sa


revision = "0020_add_discount_campaign_reason_i18n"
down_revision = "0019_add_discount_campaign_title_i18n"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("discount_campaigns", sa.Column("reason", sa.String(length=500), nullable=True))
    op.add_column("discount_campaigns", sa.Column("reason_tj", sa.String(length=700), nullable=True))
    op.add_column("discount_campaigns", sa.Column("reason_ru", sa.String(length=700), nullable=True))
    op.add_column("discount_campaigns", sa.Column("reason_uz", sa.String(length=700), nullable=True))


def downgrade() -> None:
    op.drop_column("discount_campaigns", "reason_uz")
    op.drop_column("discount_campaigns", "reason_ru")
    op.drop_column("discount_campaigns", "reason_tj")
    op.drop_column("discount_campaigns", "reason")
