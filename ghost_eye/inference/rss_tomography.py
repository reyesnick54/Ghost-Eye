"""Coarse RSS tomographic projection for WiFi-only sensing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class TomographyCell:
    """One coarse tomographic grid cell."""

    cell_id: str
    weight: float


class RssTomography:
    """Projects RSSI residuals onto preconfigured link-to-cell weights."""

    def __init__(self, link_weights: Mapping[str, Mapping[str, float]] | None = None) -> None:
        self.link_weights = {
            link.lower(): dict(weights)
            for link, weights in (link_weights or {}).items()
        }

    def project(self, residuals_db: Mapping[str, float]) -> tuple[TomographyCell, ...]:
        cell_scores: dict[str, float] = {}
        for link, residual in residuals_db.items():
            weights = self.link_weights.get(link.lower(), {})
            for cell_id, weight in weights.items():
                cell_scores[cell_id] = cell_scores.get(cell_id, 0.0) + abs(residual) * weight

        return tuple(
            TomographyCell(cell_id=cell_id, weight=score)
            for cell_id, score in sorted(
                cell_scores.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )

    def strongest_cell(
        self,
        residuals_db: Mapping[str, float],
    ) -> TomographyCell | None:
        cells = self.project(residuals_db)
        return cells[0] if cells else None


def average_cells(cells: Iterable[TomographyCell]) -> float:
    cell_tuple = tuple(cells)
    if not cell_tuple:
        return 0.0
    return sum(cell.weight for cell in cell_tuple) / len(cell_tuple)
