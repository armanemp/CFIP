"""PostgreSQL adapter for CFIP durable event dispatch."""

from .repository import PostgreSQLDurableEventRepository

__all__ = ["PostgreSQLDurableEventRepository"]
