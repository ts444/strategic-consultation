"""Chart generator — produces four PNG charts for the handover PDF."""

from __future__ import annotations

import logging
import re
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path

import matplotlib
import yaml
from matplotlib.patches import Patch

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402  (must come after matplotlib.use)

logger = logging.getLogger(__name__)

_FENCE_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)


def _parse_blocks(text: str) -> list[dict[str, object]]:
    """Extract all ```yaml fenced blocks and parse each as a YAML document."""
    blocks: list[dict[str, object]] = []
    for m in _FENCE_RE.finditer(text):
        try:
            # Use safe_load_all to handle the ---...--- document delimiters;
            # take the first non-None document which contains the block fields.
            for doc in yaml.safe_load_all(m.group(1)):
                if isinstance(doc, dict):
                    blocks.append(doc)
                    break
        except yaml.YAMLError:
            pass
    return blocks


def _chart_dir(engagement_path: Path) -> Path:
    d = engagement_path / "05-handover" / "charts"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _spend_bar(engagement_path: Path, out_dir: Path) -> Path | None:
    """Chart 1: Y1/Y2/Y3 spend stacked bar (capex + opex) from RMI/REC data."""
    roadmap_path = engagement_path / "04-roadmap" / "roadmap.md"
    rec_path = engagement_path / "03-mapping" / "recommendations.md"

    if not roadmap_path.exists():
        logger.warning("roadmap.md not found; skipping spend_bar chart")
        return None
    if not rec_path.exists():
        logger.warning("recommendations.md not found; skipping spend_bar chart")
        return None

    roadmap_blocks = _parse_blocks(roadmap_path.read_text())
    rec_blocks = _parse_blocks(rec_path.read_text())

    # Build cost lookup: REC id -> (capex £, annual_opex £)
    rec_cost: dict[str, tuple[float, float]] = {}
    for b in rec_blocks:
        raw_id = b.get("id")
        if not isinstance(raw_id, str) or not raw_id.startswith("REC-"):
            continue
        cost = b.get("cost")
        cost_dict: dict[str, object] = cost if isinstance(cost, dict) else {}
        capex_raw = cost_dict.get("capex", 0)
        opex_raw = cost_dict.get("opex_monthly", 0)
        try:
            capex_f = float(capex_raw) if capex_raw not in (None, "tbc", "") else 0.0  # type: ignore[arg-type]
        except (TypeError, ValueError):
            capex_f = 0.0
        try:
            opex_f = float(opex_raw) * 12.0 if opex_raw not in (None, "tbc", "") else 0.0  # type: ignore[arg-type]
        except (TypeError, ValueError):
            opex_f = 0.0
        rec_cost[raw_id] = (capex_f, opex_f)

    # Collect first-occurrence RECs per year (Y1 → Y2 → Y3)
    years = ["Y1", "Y2", "Y3"]
    year_recs: dict[str, list[str]] = {y: [] for y in years}
    seen_recs: set[str] = set()

    for y in years:
        for b in roadmap_blocks:
            if b.get("year") != y:
                continue
            raw_id = b.get("id")
            if not isinstance(raw_id, str) or not raw_id.startswith("RMI-"):
                continue
            addresses = b.get("addresses") or []
            if not isinstance(addresses, list):
                continue
            for ref in addresses:
                if isinstance(ref, str) and ref.startswith("REC-") and ref not in seen_recs:
                    year_recs[y].append(ref)
                    seen_recs.add(ref)

    capex_vals = [sum(rec_cost.get(r, (0.0, 0.0))[0] for r in year_recs[y]) for y in years]
    opex_vals = [sum(rec_cost.get(r, (0.0, 0.0))[1] for r in year_recs[y]) for y in years]

    fig, ax = plt.subplots(figsize=(8, 5))
    x = list(range(len(years)))
    ax.bar(x, capex_vals, label="Capex", color="#2563EB")
    ax.bar(x, opex_vals, bottom=capex_vals, label="Opex (annual)", color="#16A34A")
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylabel("£")
    ax.set_title("Estimated Spend by Year")
    ax.legend()
    plt.tight_layout()

    out = out_dir / "spend_bar.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def _gantt(engagement_path: Path, out_dir: Path) -> Path | None:
    """Chart 2: Gantt swim-lane grouped by capability phase, shaded by year."""
    roadmap_path = engagement_path / "04-roadmap" / "roadmap.md"

    if not roadmap_path.exists():
        logger.warning("roadmap.md not found; skipping gantt chart")
        return None

    blocks = _parse_blocks(roadmap_path.read_text())
    rmi_blocks = [
        b for b in blocks if isinstance(b.get("id"), str) and str(b["id"]).startswith("RMI-")
    ]

    if not rmi_blocks:
        logger.warning("No RMI blocks found; skipping gantt chart")
        return None

    phase_order = ["foundations", "enablers", "value-drivers", "optimisations"]
    year_colors = {"Y1": "#2563EB", "Y2": "#16A34A", "Y3": "#D97706"}

    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for b in rmi_blocks:
        cp = str(b.get("capability_phase", "unknown"))
        grouped[cp].append(b)

    rows: list[dict[str, object]] = []
    for phase in phase_order:
        rows.extend(grouped.get(phase, []))
    for phase, items in grouped.items():
        if phase not in phase_order:
            rows.extend(items)

    n = len(rows)
    fig, ax = plt.subplots(figsize=(10, max(4, n * 0.6 + 1)))

    year_x: dict[str, tuple[float, float]] = {"Y1": (0.0, 1.0), "Y2": (1.0, 2.0), "Y3": (2.0, 3.0)}

    for i, b in enumerate(rows):
        row_y = n - 1 - i
        year = str(b.get("year", "Y1"))
        x_s, x_e = year_x.get(year, (0.0, 1.0))
        color = year_colors.get(year, "#6B7280")
        ax.barh(row_y, x_e - x_s, left=x_s, height=0.6, color=color, alpha=0.8)
        label = f"{b.get('id', '')} — {str(b.get('title', ''))[:45]}"
        ax.text(x_s + 0.04, row_y, label, va="center", ha="left", fontsize=7, color="white")

    ax.set_yticks(list(range(n)))
    ax.set_yticklabels([str(b.get("id", "")) for b in reversed(rows)], fontsize=8)
    ax.set_xticks([0.5, 1.5, 2.5])
    ax.set_xticklabels(["Y1", "Y2", "Y3"])
    ax.set_xlim(0.0, 3.0)
    ax.set_title("Roadmap Gantt — Swim Lane by Capability Phase")

    legend_elements = [Patch(facecolor=c, label=y) for y, c in year_colors.items()]
    ax.legend(handles=legend_elements, loc="lower right")

    plt.tight_layout()
    out = out_dir / "gantt.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def _risk_donut(engagement_path: Path, out_dir: Path) -> Path | None:
    """Chart 3: Risk status donut (open / mitigated / accepted / closed)."""
    risks_path = engagement_path / "_risks.md"

    if not risks_path.exists():
        logger.warning("_risks.md not found; skipping risk_donut chart")
        return None

    blocks = _parse_blocks(risks_path.read_text())
    rsk_blocks = [
        b for b in blocks if isinstance(b.get("id"), str) and str(b["id"]).startswith("RSK-")
    ]

    if not rsk_blocks:
        logger.warning("No RSK blocks found; skipping risk_donut chart")
        return None

    status_order = ["open", "mitigated", "accepted", "closed"]
    counts: dict[str, int] = {s: 0 for s in status_order}
    for b in rsk_blocks:
        status = str(b.get("status", "open")).strip()
        if status in counts:
            counts[status] += 1
        else:
            counts["open"] += 1

    labels = [s for s in status_order if counts[s] > 0]
    sizes = [counts[s] for s in labels]
    palette = {
        "open": "#EF4444", "mitigated": "#3B82F6", "accepted": "#F59E0B", "closed": "#10B981"
    }
    chart_colors = [palette[lb] for lb in labels]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        sizes,
        labels=labels,
        colors=chart_colors,
        autopct="%1.0f%%",
        pctdistance=0.7,
        wedgeprops={"width": 0.5},
    )
    ax.set_title("Risk Register Status")

    plt.tight_layout()
    out = out_dir / "risk_donut.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def _gap_coverage(engagement_path: Path, out_dir: Path) -> Path | None:
    """Chart 4: Horizontal bar per gap coloured by mapping outcome."""
    gaps_path = engagement_path / "02-gap" / "gaps.md"
    service_map_path = engagement_path / "03-mapping" / "service-map.md"
    rec_path = engagement_path / "03-mapping" / "recommendations.md"

    if not gaps_path.exists():
        logger.warning("gaps.md not found; skipping gap_coverage chart")
        return None
    if not service_map_path.exists():
        logger.warning("service-map.md not found; skipping gap_coverage chart")
        return None

    gap_blocks = [
        b for b in _parse_blocks(gaps_path.read_text())
        if isinstance(b.get("id"), str) and str(b["id"]).startswith("GAP-")
    ]
    map_blocks = [
        b for b in _parse_blocks(service_map_path.read_text())
        if isinstance(b.get("id"), str) and str(b["id"]).startswith("MAP-")
    ]

    # Build REC lookup: service_name -> compliance_relation
    svc_relation: dict[str, str] = {}
    if rec_path.exists():
        for b in _parse_blocks(rec_path.read_text()):
            if isinstance(b.get("id"), str) and str(b["id"]).startswith("REC-"):
                svc = str(b.get("proposed_service", ""))
                relation = str(b.get("compliance_relation", "addresses"))
                if svc:
                    svc_relation[svc] = relation

    # Collect MAP data per gap
    gap_data: dict[str, dict[str, object]] = {}
    for b in map_blocks:
        gap_id = str(b.get("gap", ""))
        if not gap_id.startswith("GAP-"):
            continue
        service = str(b.get("proposed_service", ""))
        curated_raw = b.get("curated", False)
        curated = bool(curated_raw) if not isinstance(curated_raw, bool) else curated_raw

        if gap_id not in gap_data:
            gap_data[gap_id] = {"has_no_known": False, "curated_services": [], "has_curated": False}

        entry = gap_data[gap_id]
        curated_list = entry["curated_services"]
        assert isinstance(curated_list, list)

        if service == "[no-known-service]":
            entry["has_no_known"] = True
        elif curated:
            curated_list.append(service)
            entry["has_curated"] = True

    # Determine outcome per gap
    gap_outcome: dict[str, str] = {}
    for gap_id, data in gap_data.items():
        if data["has_no_known"]:
            gap_outcome[gap_id] = "no-known-service"
        elif data["has_curated"]:
            svcs = data["curated_services"]
            assert isinstance(svcs, list)
            fully = all(
                svc_relation.get(str(s), "addresses") != "partially-addresses" for s in svcs
            )
            gap_outcome[gap_id] = "fully-mapped" if fully else "partially-mapped"
        else:
            gap_outcome[gap_id] = "partially-mapped"

    gap_titles = {str(b["id"]): str(b.get("title", b["id"])) for b in gap_blocks}
    gap_ids = sorted(gap_titles.keys())

    if not gap_ids:
        logger.warning("No GAP blocks found; skipping gap_coverage chart")
        return None

    outcome_colors = {
        "fully-mapped": "#16A34A",
        "partially-mapped": "#F59E0B",
        "no-known-service": "#EF4444",
    }

    n = len(gap_ids)
    fig, ax = plt.subplots(figsize=(10, max(4, n * 0.6 + 1)))

    for i, gap_id in enumerate(gap_ids):
        outcome = gap_outcome.get(gap_id, "no-known-service")
        color = outcome_colors.get(outcome, "#6B7280")
        ax.barh(i, 1.0, color=color, alpha=0.85, height=0.6)
        ax.text(
            0.02, i, gap_id, va="center", ha="left", fontsize=8, color="white", fontweight="bold"
        )

    ax.set_yticks(list(range(n)))
    ax.set_yticklabels([gap_titles.get(g, g)[:55] for g in gap_ids], fontsize=8)
    ax.set_xticks([])
    ax.set_title("Gap Coverage by Mapping Outcome")

    legend_elements = [
        Patch(facecolor=c, label=lb.replace("-", " ")) for lb, c in outcome_colors.items()
    ]
    ax.legend(handles=legend_elements, loc="lower right")

    plt.tight_layout()
    out = out_dir / "gap_coverage.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def generate_charts(engagement_path: Path) -> dict[str, Path]:
    """Generate four handover charts; return mapping of chart name to PNG path."""
    out_dir = _chart_dir(engagement_path)
    results: dict[str, Path] = {}

    chart_fns: list[tuple[str, Callable[[Path, Path], Path | None]]] = [
        ("spend_bar", _spend_bar),
        ("gantt", _gantt),
        ("risk_donut", _risk_donut),
        ("gap_coverage", _gap_coverage),
    ]

    for name, fn in chart_fns:
        try:
            path = fn(engagement_path, out_dir)
            if path is not None:
                results[name] = path
        except Exception:
            logger.warning("Failed to generate %s chart", name, exc_info=True)

    return results
