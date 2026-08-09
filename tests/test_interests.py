"""Unit tests for scripts/interests.py — the 13-cluster taxonomy seam."""

from __future__ import annotations

from pathlib import Path

import interests as ii
import pytest
from conftest import make_entry

REPO_INTERESTS = Path(__file__).resolve().parent.parent / "data" / "interests.yaml"


def test_load_interests_returns_all_thirteen_clusters():
    tax = ii.load_interests(REPO_INTERESTS)
    assert set(tax.clusters) == set("ABCDEFGHIJKLM")
    assert len(tax.clusters) == 13


def test_every_cluster_has_name_description_and_scope():
    tax = ii.load_interests(REPO_INTERESTS)
    for letter, cluster in tax.clusters.items():
        assert cluster.name, f"cluster {letter} missing name"
        assert cluster.description, f"cluster {letter} missing description"
        assert cluster.scope, f"cluster {letter} missing scope bullets"


def test_defender_scope_present_on_e_and_d():
    """Regression guard on the taxonomy correction: E (prompt injection) and
    D (model supply chain) must include defender-side scope, not just attacks."""
    tax = ii.load_interests(REPO_INTERESTS)
    e_scope = " ".join(tax.clusters["E"].scope).lower()
    d_scope = " ".join(tax.clusters["D"].scope).lower()
    assert "defender" in e_scope or "containment" in e_scope
    assert "defender" in d_scope or "admission-gate" in d_scope


def test_security_native_clusters_exist():
    """K/L/M were the taxonomy correction — enforce their presence."""
    tax = ii.load_interests(REPO_INTERESTS)
    assert "threat model" in tax.clusters["K"].name.lower()
    assert "red-team" in tax.clusters["L"].name.lower()
    assert "tooling" in tax.clusters["M"].name.lower()


def test_cluster_for_reads_entry_cluster_field():
    """The analyzer emits `cluster: <letter>` per finding; interests.cluster_for
    returns the letter (or None if the entry is adjacent)."""
    tax = ii.load_interests(REPO_INTERESTS)
    assert ii.cluster_for(make_entry(cluster="A"), tax) == "A"
    assert ii.cluster_for(make_entry(cluster="M"), tax) == "M"
    assert ii.cluster_for(make_entry(cluster=None), tax) is None
    # Missing field is treated as adjacent, not an error — analyzer may not have
    # emitted a cluster yet on legacy entries.
    entry_no_cluster = make_entry()
    entry_no_cluster.pop("cluster", None)
    assert ii.cluster_for(entry_no_cluster, tax) is None


def test_cluster_for_rejects_unknown_letter():
    """A cluster letter not in the taxonomy is invalid input — the entry is
    treated as adjacent so downstream routing can't cite a nonexistent cluster."""
    tax = ii.load_interests(REPO_INTERESTS)
    assert ii.cluster_for(make_entry(cluster="Z"), tax) is None
    assert ii.cluster_for(make_entry(cluster="a"), tax) is None  # case-sensitive


def test_is_tier1_true_for_in_cluster_entries():
    tax = ii.load_interests(REPO_INTERESTS)
    for letter in "ABCDEFGHIJKLM":
        assert ii.is_tier1(make_entry(cluster=letter), tax), letter


def test_is_tier1_false_for_adjacent_entries():
    tax = ii.load_interests(REPO_INTERESTS)
    assert not ii.is_tier1(make_entry(cluster=None), tax)
    entry_no_cluster = make_entry()
    entry_no_cluster.pop("cluster", None)
    assert not ii.is_tier1(entry_no_cluster, tax)


def test_adjacent_and_excluded_lists_present():
    """Adjacent + excluded lists are prompt-context for the analyzer — the
    module must expose them, not silently drop them."""
    tax = ii.load_interests(REPO_INTERESTS)
    assert tax.adjacent  # non-empty list of strings
    assert tax.excluded
    assert all(isinstance(x, str) for x in tax.adjacent)
    assert all(isinstance(x, str) for x in tax.excluded)


def test_load_interests_raises_on_missing_file(tmp_path):
    missing = tmp_path / "does-not-exist.yaml"
    with pytest.raises(FileNotFoundError):
        ii.load_interests(missing)


def test_load_interests_raises_on_malformed_shape(tmp_path):
    """A file present but missing `clusters:` is a bug, not a soft default —
    silently treating everything as adjacent would hide a config error."""
    bad = tmp_path / "bad.yaml"
    bad.write_text("version: 1\n", encoding="utf-8")
    with pytest.raises(ValueError):
        ii.load_interests(bad)
