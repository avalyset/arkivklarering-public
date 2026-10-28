#!/usr/bin/env python3
"""DEV: sammenligner inaSpeechSegmenter (ny kjører, `arkivklarering.segment_inaseg`) med inaVAMOS-tidslinjene som ALLEREDE ligger på disk.

Kjører IKKE inaVAMOS (ingen import, ingen kall) og leser ingen testdata. Leser bare eksisterende filer:
  - `eval-data/ord_nbsamtale_validation.jsonl` (inaVAMOS-cachen, `felles.cache_sti(..., segmentering="inavamos")`; 60 NB Samtale validation-segmenter, DEV; `tidslinje` per segment),
  - `ut/rokytest.segments.json` og `ut/rokytest_personvern.segments.json` (røyktestlydene i `lyd/`).
Disse inneholder inaVAMOS-utdata etter `segment.bygg_tidslinje` (sammenslåing av tale over gap ≤ 1 s; ikke inaVAMOS' rå etiketter). Den nye kjørerens utdata
sendes gjennom samme `bygg_tidslinje`, så sammenligningen er epler mot epler. Lydfilene er de samme.

    PYTHONPATH=. .venv/bin/python eval/dev/sammenlign_inaseg_dev.py [--hoved ~/dev/arkivklarering]   (etter `source scripts/miljo.sh`)
"""
import argparse
import collections
import datetime
import json
import pathlib
import sys
import time
import wave

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "eval" / "dev"))
from arkivklarering import miljo, segment, segment_inaseg  # noqa: E402
import felles  # noqa: E402

# Bevisst inaVAMOS-cachen (det er den som sammenlignes med), uansett ARKIVKLARERING_SEGMENTERING: _inavamos-fila eller den eldre fila uten
# suffiks, som er laget med inaVAMOS (felles.cache_sti)
CACHE = felles.cache_sti(miljo.EVAL_DATA, "ord_nbsamtale_validation", segmentering="inavamos")
LYD_DEV = miljo.EVAL_DATA / "nb_samtale" / "valg_validation"
GAMLE = ("speech", "speech+music", "music", "other")
NYE = ("speech", "music", "other")


def varighet(sti):
    with wave.open(str(sti), "rb") as w:
        return w.getnframes() / w.getframerate()


def overlapp(a, b):
    return max(0.0, min(a[1], b[1]) - max(a[0], b[0]))


def segs_fra_dict(tl):
    return [{"label": s["label"], "start": s["start"], "stopp": s["stopp"], "disposisjon": s["disposisjon"],
             "mus": s.get("musikk_under_tale", [])} for s in tl]


def segs_fra_ny(raa):
    return [{"label": s.label, "start": s.start, "stopp": s.stop, "disposisjon": s.disposisjon, "mus": s.musikk_under_tale}
            for s in segment.bygg_tidslinje(raa)]


def matrise(gammel, ny, matr):
    for g in gammel:
        for n in ny:
            o = overlapp((g["start"], g["stopp"]), (n["start"], n["stopp"]))
            if o:
                matr[(g["label"], n["label"])] += o


def transkribert(tl):
    return [(s["start"], s["stopp"]) for s in tl if s["disposisjon"] == segment.TRANSKRIBER]


def sum_overlapp(iv, andre):
    return sum(overlapp(a, b) for a in iv for b in andre)


def sammenlign(filer, gml, nye_tl):
    """filer: [id]; gml/nye_tl: {id: [segmentdict]}. Returnerer (rapportdict)."""
    matr = collections.Counter()
    pr_fil, bare_gml_seg, bare_ny_seg = [], [], []
    sm_intervaller = []
    for f in filer:
        matrise(gml[f], nye_tl[f], matr)
        tg, tn = transkribert(gml[f]), transkribert(nye_tl[f])
        sg, sn = sum(b - a for a, b in tg), sum(b - a for a, b in tn)
        felles = sum_overlapp(tg, tn)
        pr_fil.append({"id": f, "transkribert_gammel_s": round(sg, 2), "transkribert_ny_s": round(sn, 2), "bare_gammel_s": round(sg - felles, 2),
                       "bare_ny_s": round(sn - felles, 2), "binaer_ulik": (sg > 0) != (sn > 0)})
        for a, b in tg:  # inaVAMOS-segmenter som ville falt bort
            if sum_overlapp([(a, b)], tn) < 0.5 * (b - a):
                bare_gml_seg.append({"id": f, "start": a, "stopp": b})
        for a, b in tn:
            if sum_overlapp([(a, b)], tg) < 0.5 * (b - a):
                bare_ny_seg.append({"id": f, "start": a, "stopp": b})
        for g in gml[f]:
            if g["label"] == "speech+music":
                nye_pa_segmentet, nye_pa_musikk = collections.Counter(), collections.Counter()
                for n in nye_tl[f]:
                    o = overlapp((g["start"], g["stopp"]), (n["start"], n["stopp"]))
                    if o:
                        nye_pa_segmentet[n["label"]] += o
                    for m in g["mus"]:
                        om = overlapp(tuple(m), (n["start"], n["stopp"]))
                        if om:
                            nye_pa_musikk[n["label"]] += om
                sm_intervaller.append({"id": f, "start": g["start"], "stopp": g["stopp"], "varighet_s": round(g["stopp"] - g["start"], 3),
                                       "musikk_under_tale": g["mus"], "ny_etikett_pa_segmentet_s": {k: round(v, 3) for k, v in nye_pa_segmentet.items()},
                                       "ny_etikett_pa_musikkintervallene_s": {k: round(v, 3) for k, v in nye_pa_musikk.items()},
                                       "ny_disposisjon_transkriber_s": round(sum_overlapp([(g["start"], g["stopp"])], tn), 3)})
    tot = sum(matr.values())
    per_gammel = {}
    for g in GAMLE:
        rad = {n: round(matr[(g, n)], 2) for n in NYE}
        s = sum(rad.values())
        ekv = {"speech+music": "speech"}.get(g, g)
        per_gammel[g] = {"sekunder": round(s, 2), "ny": rad, "andel_ny": {n: round(rad[n] / s, 4) if s else None for n in NYE},
                         "enig_streng": round(rad.get(g, 0) / s, 4) if s and g in NYE else (0.0 if s else None),
                         "enig_tale_ekvivalent": round(rad.get(ekv, 0) / s, 4) if s else None}
    enig_streng = sum(matr[(g, g)] for g in NYE)
    enig_ekv = sum(matr[(g, {"speech+music": "speech"}.get(g, g))] for g in GAMLE)
    return {"filer": len(filer), "sekunder_sammenlignet": round(tot, 2), "enighet_streng_andel": round(enig_streng / tot, 4) if tot else None,
            "enighet_tale_ekvivalent_andel": round(enig_ekv / tot, 4) if tot else None, "per_gammel_etikett": per_gammel,
            "transkripsjon": {"filer_binaer_ulik": sum(p["binaer_ulik"] for p in pr_fil),
                              "filer_med_minst_0_5_s_forskjell": sum((p["bare_gammel_s"] + p["bare_ny_s"]) >= 0.5 for p in pr_fil),
                              "sekunder_bare_inavamos": round(sum(p["bare_gammel_s"] for p in pr_fil), 2),
                              "sekunder_bare_ny": round(sum(p["bare_ny_s"] for p in pr_fil), 2),
                              "segmenter_bare_inavamos_transkribert": len(bare_gml_seg), "segmenter_bare_ny_transkribert": len(bare_ny_seg),
                              "per_fil": pr_fil},
            "speech_music_intervaller": sm_intervaller}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hoved", default=str(pathlib.Path.home() / "dev/arkivklarering"), help="repoet der ut/ og lyd/ (røyktesten) ligger")
    a = ap.parse_args()
    hoved = pathlib.Path(a.hoved)
    ut = {}
    # --- DEV: NB Samtale validation (60 segmenter)
    celler = [json.loads(l) for l in CACHE.read_text(encoding="utf-8").splitlines() if l.strip()]
    lyd = {p.stem: p for p in LYD_DEV.rglob("*.wav")}
    ider = [c["id"] for c in celler]
    assert all(i in lyd for i in ider), "DEV-lyd mangler"
    gml = {c["id"]: segs_fra_dict(c["tidslinje"]) for c in celler}
    dur = {i: varighet(lyd[i]) for i in ider}
    t0 = time.time()
    raa = segment_inaseg.segmenter_flere([lyd[i] for i in ider])
    t60 = time.time() - t0
    t0 = time.time()
    segment_inaseg.segmenter_flere([lyd[ider[0]]])
    t1 = time.time() - t0
    nye = {i: segs_fra_ny(r) for i, r in zip(ider, raa)}
    ut["nbsamtale_validation"] = sammenlign(ider, gml, nye)
    tot_s = sum(dur.values())
    ut["fart"] = {"filer": len(ider), "lyd_s": round(tot_s, 1), "tid_60_filer_s": round(t60, 1), "tid_1_fil_s": round(t1, 1),
                  "marginal_s_per_fil": round((t60 - t1) / (len(ider) - 1), 3), "marginal_s_per_lydsekund": round((t60 - t1) / (tot_s - dur[ider[0]]), 4),
                  "oppstart_s": round(t1 - ((t60 - t1) / (len(ider) - 1)) * 1, 1)}
    # --- røyktestlydene
    rok = {}
    for navn in ("rokytest", "rokytest_personvern"):
        sti = next(s for s in (hoved / "ut" / f"{navn}.segments.json", hoved / "ut" / navn / f"{navn}.segments.json") if s.is_file())
        g = json.loads(sti.read_text(encoding="utf-8"))["segmenter"]
        gml_r = {navn: [{"label": s["label"], "start": s["start"], "stopp": s["stopp"], "disposisjon": s["disposisjon"],
                         "mus": s.get("musikk_under_tale", [])} for s in g]}
        r = segment_inaseg.segmenter_flere([hoved / "lyd" / f"{navn}.wav"])[0]
        rok[navn] = sammenlign([navn], gml_r, {navn: segs_fra_ny(r)})
        rok[navn]["ny_tidslinje"] = [(s["label"], round(s["start"], 2), round(s["stopp"], 2), s["disposisjon"]) for s in segs_fra_ny(r)]
        rok[navn]["gammel_tidslinje"] = [(s["label"], round(s["start"], 2), round(s["stopp"], 2), s["disposisjon"]) for s in gml_r[navn]]
    ut["rokytest"] = rok
    ut["merknad"] = ("DEV og røyktest, ikke testdata. inaVAMOS ble ikke kjørt: gamle utdata er lest fra filene som lå på disk (tidslinje etter bygg_tidslinje). "
                     "Nye utdata er inaSpeechSegmenter 0.8.0 (smn, uten kjønn) → etikettkart → samme bygg_tidslinje.")
    ut["laget"] = datetime.datetime.now().isoformat(timespec="seconds")
    (REPO / "eval/dev/inaseg_sammenligning_dev_2026-10-27.json").write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in ut.items() if k not in ("nbsamtale_validation", "rokytest")}, ensure_ascii=False))
    print("skrevet eval/dev/inaseg_sammenligning_dev_2026-10-27.json")


if __name__ == "__main__":
    main()
