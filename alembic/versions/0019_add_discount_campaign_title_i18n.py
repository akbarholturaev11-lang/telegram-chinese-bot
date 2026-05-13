"""add discount campaign title i18n

Revision ID: 0019_add_discount_campaign_title_i18n
Revises: 0018_add_discount_campaigns
Create Date: 2026-05-13
"""

from alembic import op
import sqlalchemy as sa


revision = "0019_add_discount_campaign_title_i18n"
down_revision = "0018_add_discount_campaigns"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("discount_campaigns", sa.Column("title_tj", sa.String(length=180), nullable=True))
    op.add_column("discount_campaigns", sa.Column("title_ru", sa.String(length=180), nullable=True))
    op.add_column("discount_campaigns", sa.Column("title_uz", sa.String(length=180), nullable=True))


def downgrade() -> None:
    op.drop_column("discount_campaigns", "title_uz")
    op.drop_column("discount_campaigns", "title_ru")
    op.drop_column("discount_campaigns", "title_tj")
