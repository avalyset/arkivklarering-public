import hashlib
import pathlib
import re

V = pathlib.Path(__file__).resolve().parent.parent / "arkivklarering" / "_vendor" / "norsk_tale"


def test_vendor_filene_er_uendret_fra_origin():
    origin = (V / "ORIGIN.txt").read_text(encoding="utf-8")
    forventet = dict((n, h) for h, n in re.findall(r"^\s+([0-9a-f]{64})\s+(\S+)$", origin, re.M))
    assert set(forventet) == {"norm.py", "score.py"}
    for navn, h in forventet.items():
        assert hashlib.sha256((V / navn).read_bytes()).hexdigest() == h, f"{navn} er endret i forhold til ORIGIN.txt"
    assert "bcfef63d1be49ac239956dfb67784c002cecf310" in origin and (V / "LICENSE").exists()
