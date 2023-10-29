from typing import Literal
from litestar.dto.config import DTOConfig
from litestar.dto import DataclassDTO, dto_field
from collections.abc import Set as AbstractSet
from litestar.dto import RenameStrategy


def config(
    backend: Literal["dataclass", "sqlalchemy"] = "dataclass",
    exclude: AbstractSet[str] | None = None,
    rename_fields: dict[str, str] | None = None,
    rename_strategy: RenameStrategy = None,
    max_nested_depth: int | None = None,
    partial: bool | None = None,
) -> DTOConfig:
    """_summary_

    Returns:
        DTOConfig: Configured DTO class
    """
    default_kwargs = {"rename_strategy": "camel", "max_nested_depth": 2}
    if exclude:
        default_kwargs["exclude"] = exclude
    if rename_fields:
        default_kwargs["rename_fields"] = rename_fields
    if rename_strategy:
        default_kwargs["rename_strategy"] = rename_strategy
    if max_nested_depth:
        default_kwargs["max_nested_depth"] = max_nested_depth
    if partial:
        default_kwargs["partial"] = partial
    return DTOConfig(**default_kwargs)
