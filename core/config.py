"""
GeoResearchAgent-247 Configuration Manager
Loads and validates agent configuration from YAML files and environment variables.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class BackendConfig(BaseModel):
    orchestrator: str = "claude-sonnet-4-6"
    coding_workers: CodingWorkerConfig = Field(default_factory=lambda: CodingWorkerConfig())


class CodingWorkerConfig(BaseModel):
    provider: Literal["claude", "openai"] = "claude"
    model: str = "claude-sonnet-4-6"
    max_workers: int = 1
    task_types: list[str] = Field(default_factory=lambda: ["code_generation", "data_analysis", "plotting"])


class LiteratureConfig(BaseModel):
    max_papers: int = 30
    sources: list[str] = Field(default_factory=lambda: ["arxiv", "semantic_scholar"])
    geo_query_expansion: bool = True  # adds geo-specific terms to queries
    recency_weight: float = 0.3       # 0 = ignore date, 1 = only recent


class ExperimentConfig(BaseModel):
    max_iterations: int = 3
    sandbox_timeout_sec: int = 300
    auto_install_packages: bool = True
    save_intermediate: bool = True


class WritingConfig(BaseModel):
    temperature: float = 0.7
    journal: str = "IJGIS"
    output_format: Literal["markdown", "latex", "pdf"] = "markdown"
    review_rounds: int = 2


class OutputConfig(BaseModel):
    base_dir: str = "output"
    checkpoint_dir: str = ".checkpoints"
    log_dir: str = "harness/logs"
    save_intermediate: bool = True


class AgentConfig(BaseModel):
    """Top-level configuration for GeoResearchAgent-247."""

    mode: Literal["quick", "full-auto", "codex-hybrid", "benchmark-only", "partial"] = "quick"
    topic: str = ""
    enabled_agents: list[str] = Field(
        default_factory=lambda: ["literature", "experiment", "writing", "review", "geo_specialist"]
    )
    backend: BackendConfig = Field(default_factory=BackendConfig)
    literature: LiteratureConfig = Field(default_factory=LiteratureConfig)
    experiment: ExperimentConfig = Field(default_factory=ExperimentConfig)
    writing: WritingConfig = Field(default_factory=WritingConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)


def load_config(config_path: str | Path) -> AgentConfig:
    """Load configuration from a YAML file, with environment variable overrides."""
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        raw = yaml.safe_load(f)

    # Environment variable overrides
    if topic := os.getenv("GEO_AGENT_TOPIC"):
        raw.setdefault("topic", topic)
    if output_dir := os.getenv("GEO_AGENT_OUTPUT_DIR"):
        raw.setdefault("output", {})["base_dir"] = output_dir

    return AgentConfig.model_validate(raw)


def get_default_config() -> AgentConfig:
    """Return default configuration."""
    return AgentConfig()
