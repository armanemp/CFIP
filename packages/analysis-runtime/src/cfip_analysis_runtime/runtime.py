"""Bounded deterministic engine registry/execution boundary."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from time import monotonic
from typing import Awaitable, Callable

from .models import EngineDescriptor, EngineExecutionContext, EngineOutput, FailurePolicy


EngineCallable = Callable[[EngineExecutionContext], Awaitable[EngineOutput]]


class UnknownEngineError(LookupError):
    """Raised when an exact engine/version is not registered."""


class DuplicateEngineError(ValueError):
    """Raised when an engine identity is registered more than once."""


@dataclass(frozen=True, slots=True)
class EngineHealth:
    executions: int
    failures: int
    timeouts: int
    last_latency_ms: float | None

    @property
    def failure_rate(self) -> float:
        return self.failures / self.executions if self.executions else 0.0


@dataclass(slots=True)
class _Registration:
    descriptor: EngineDescriptor
    execute: EngineCallable
    executions: int = 0
    failures: int = 0
    timeouts: int = 0
    last_latency_ms: float | None = None

    def health(self) -> EngineHealth:
        return EngineHealth(self.executions, self.failures, self.timeouts, self.last_latency_ms)


class EngineRuntime:
    """Register and execute canonical engines with explicit bounded semantics."""

    def __init__(
        self,
        registrations: tuple[tuple[EngineDescriptor, EngineCallable], ...] = (),
        *,
        max_concurrency: int = 8,
    ) -> None:
        if max_concurrency <= 0:
            raise ValueError("max_concurrency must be > 0")
        self._registrations: dict[tuple[str, str], _Registration] = {}
        self._semaphore = asyncio.Semaphore(max_concurrency)
        for descriptor, execute in registrations:
            self.register(descriptor, execute)

    def register(self, descriptor: EngineDescriptor, execute: EngineCallable) -> None:
        if descriptor.key in self._registrations:
            raise DuplicateEngineError(descriptor.key)
        self._registrations[descriptor.key] = _Registration(descriptor, execute)

    def descriptor(self, engine_id: str, version: str | None = None) -> EngineDescriptor:
        if version is not None:
            registration = self._registrations.get((engine_id, version))
            if registration is None:
                raise UnknownEngineError((engine_id, version))
            return registration.descriptor
        matches = [r for r in self._registrations.values() if r.descriptor.engine_id == engine_id]
        if not matches:
            raise UnknownEngineError(engine_id)
        return max(matches, key=lambda r: self._version_key(r.descriptor.version)).descriptor

    @staticmethod
    def _version_key(version: str) -> tuple[int, ...]:
        """Compare numeric dotted versions without introducing a dependency."""
        try:
            parts = tuple(int(part) for part in version.split("."))
        except ValueError:
            return (-1,)
        return parts

    def health(self, engine_id: str, version: str) -> EngineHealth:
        registration = self._registrations.get((engine_id, version))
        if registration is None:
            raise UnknownEngineError((engine_id, version))
        return registration.health()

    def descriptors(self) -> tuple[EngineDescriptor, ...]:
        return tuple(r.descriptor for r in self._registrations.values())

    async def execute(self, engine_id: str, version: str, context: EngineExecutionContext) -> EngineOutput | None:
        registration = self._registrations.get((engine_id, version))
        if registration is None:
            raise UnknownEngineError((engine_id, version))
        descriptor = registration.descriptor
        if context.timeframe not in descriptor.supported_timeframes:
            raise ValueError(f"unsupported timeframe: {context.timeframe}")

        async with self._semaphore:
            registration.executions += 1
            started = monotonic()
            try:
                result = await asyncio.wait_for(
                    registration.execute(context),
                    timeout=descriptor.latency_budget_ms / 1000,
                )
            except asyncio.TimeoutError:
                registration.timeouts += 1
                registration.failures += 1
                registration.last_latency_ms = (monotonic() - started) * 1000
                if descriptor.failure_policy is FailurePolicy.FAIL_CLOSED:
                    raise
                return None
            except Exception:
                registration.failures += 1
                registration.last_latency_ms = (monotonic() - started) * 1000
                if descriptor.failure_policy is FailurePolicy.FAIL_CLOSED:
                    raise
                return None

            registration.last_latency_ms = (monotonic() - started) * 1000
            if result.engine_id != descriptor.engine_id or result.version != descriptor.version:
                raise ValueError("engine output identity does not match descriptor")
            if result.data_revision != context.data_revision:
                raise ValueError("engine output data_revision does not match execution context")
            return result

    async def execute_many(
        self,
        requests: tuple[tuple[str, str, EngineExecutionContext], ...],
    ) -> tuple[EngineOutput, ...]:
        """Execute independent engines concurrently under bounded concurrency."""
        results = await asyncio.gather(*(self.execute(*request) for request in requests))
        return tuple(result for result in results if result is not None)
