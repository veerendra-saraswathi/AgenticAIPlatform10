"""
Distributed Runtime Layer for AgenticAIPlatform10

This package provides infrastructure-level adapters that allow
existing Agentic AI workflows and agents to execute in
distributed environments (Ray / Anyscale / KubeRay) WITHOUT
modifying core agent logic.

Design principles:
- Core domain logic stays pure
- Distribution is a runtime concern
- Agents are wrapped, never rewritten
"""
