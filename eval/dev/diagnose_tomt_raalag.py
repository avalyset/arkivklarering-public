#!/usr/bin/env python3
"""Diagnose: hvorfor ga rålaget tom eller kort utdata på noen ren NB Samtale validation-segmenter i «før»-kjøringen av KLAR-EVAL-0010?

Tar segmentene der rålagets utdata i `deg_original.jsonl` eller `deg_degradert.jsonl` har under halvparten av referanseordene, kutter de samme
talesegmentene (tidslinjen fra cachen, samme `_kutt` som rørledningen) og kjører whisper-cli på dem med varianter som tester én hypotese
om gangen. Alle kjøringer er én whisper-cli-prosess om gangen. V0 kjører hver fil i egen prosess med en debug-bygget whisper-cli (samme kilde, `-DWHISPER_DEBUG`,
bygget i en egen mappe) for å få whisper.cpps egne beslutningslinjer; de øvrige variantene kjører alle filene i én prosess med `-mc 0` (ingen
tekstkontekst fra forrige fil) for å spare modell-lasting, og V0b/V8 viser at det ikke endrer utfallet / at kontekst mellom filer gjør det. Skriver `eval/dev/diagnose_tomt_raalag_<dato>.json` (tall og tekst per
variant), og full stderr per kjøring ligger under $ARKIVKLARERING_DATA/tmp/diag/. Tidslinjen leses fra cachen for gjeldende segmentering
(`felles.cache_sti`): resultatet fra 26.10 bygger på inaVAMOS-cachene, så gjenskaping krever ARKIVKLARERING_SEGMENTERING=inavamos.

    source scripts/miljo.sh && .venv/bin/python eval/dev/diagnose_tomt_raalag.py
"""
import datetime
import json
import pathlib
import re
import subprocess
import sys

HER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HER))
import felles  # noqa: E402
import jiwer  # noqa: E402
import kjor_flaggoverlevelse_ord as fo  # noqa: E402
from felles import les_jsonl  # noqa: E402

from arkivklarering import miljo, transkriber  # noqa: E402
from arkivklarering.segment import Segment  # noqa: E402

REPO = HER.parent.parent
CACHE = miljo.EVAL_DATA
ARB = miljo.DATA / "tmp" / "diag"
DATO = datetime.date.today().isoformat()
SPRAK = {"nb": "no", "nn": "nn"}
DEBUG_CLI = miljo.DATA / "tmp" / "whisper-debug-build" / "bin" / "whisper-cli"
DEBUGLINJER = re.compile(r"failed|no_speech|avg_logprob|temperature = |best decoder|detected|lang_id|is_no_speech|decoding with", re.I)


def norm(t):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", t.lower())).strip()


def tekst_fra_json(js):
    return " ".join(s.get("text", "").strip() for s in js.get("transcription", [])).strip()


def kjor(o, wavs, sprak, ekstra, med_np=True, label="", cli=None):
    """Én whisper-cli-prosess på `wavs`. Returnerer (json per fil, stderr)."""
    argv = [str(cli or o.whisper_cli), "-l", sprak, "-m", o.modell, "-oj", *(["-np"] if med_np else []), *ekstra]
    for w in wavs:
        argv += ["-f", str(w)]
        pathlib.Path(f"{w}.json").unlink(missing_ok=True)
    felles.vent_pa_ressurser(lambda *a: print(*a, flush=True))
    r = subprocess.run(argv, capture_output=True, text=True, errors="replace", timeout=1200)
    js = []
    for w in wavs:
        p = pathlib.Path(f"{w}.json")
        js.append(json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"transcription": [], "feil": f"rc={r.returncode}"})
    return js, r.stderr, " ".join(argv)


def main():
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()
    bare = sys.argv[1].split(",") if len(sys.argv) > 1 else None  # f.eks. V10,V11,V12: kjør bare disse og legg dem til i eksisterende rapport
    items = {i["id"]: i for i in fo.items_nbsamtale()}
    for i in items.values():
        i["whisper_sprak"] = SPRAK[i["gruppe"]]
    a = les_jsonl(felles.cache_sti(CACHE, "deg_original"))  # tidslinjen følger segmenteringen (felles.cache_sti)
    b = les_jsonl(felles.cache_sti(CACHE, "deg_degradert"))
    if not a or not b:
        sys.exit(f"mangler cache for segmenteringen {felles.segment.valgt_segmentering()}: {felles.cache_sti(CACHE, 'deg_original').name}, "
                 f"{felles.cache_sti(CACHE, 'deg_degradert').name} (kjør eval/dev/kjor_degradering.py først)")
    h = lambda c: norm(" ".join(x["tekst"] for x in c["cues"]["ra"]))  # noqa: E731
    ids = [k for k, i in items.items()
           if len(h(a[k]).split()) < 0.5 * len(norm(i["ref"]).split()) or len(h(b[k]).split()) < 0.5 * len(norm(i["ref"]).split())]
    print(f"{len(ids)} segmenter med rålagsutdata under halvparten av referanseordene (original eller degradert): {ids}", flush=True)
    ra = transkriber.finn_oppsett("ra")
    no = transkriber.finn_oppsett("normalisert")
    ARB.mkdir(parents=True, exist_ok=True)
    wavs = {}
    for k in ids:
        wavs[k] = []
        for n, s in enumerate(s for s in a[k]["tidslinje"] if s["disposisjon"] == "transkriber"):
            w = ARB / f"{k}_{n}.wav"
            transkriber._kutt(items[k]["lyd"], s["start"], s["stopp"], w)
            wavs[k].append((w, s))
        # hele ytringen uten segmentering (hypotese f)

    DTW = ["-nfa", "-dtw", "large.v3", "-ojf"]
    VARIANTER = [  # (navn, hypotese, laget, ekstra-argumenter, språk=None → matchet, modus: "isolert" | "batch" | "batch_kontekst", cli)
        ("V0 slik rørledningen kjører, én fil per prosess, debug-bygget whisper-cli", "referanse (med beslutningslinjer)", ra, DTW, None, "isolert", DEBUG_CLI),
        ("V0b alle filer i én prosess, -mc 0 (ingen kontekst)", "kontroll: gir batch uten kontekst samme som isolert?", ra, DTW + ["-mc", "0"], None, "batch", None),
        ("V8 alle filer i én prosess, standard kontekst", "g: tekstkontekst fra forrige fil", ra, DTW, None, "batch", None),
        ("V1 uten DTW (-mc 0)", "e: ordtidsstempel-modus", ra, ["-mc", "0"], None, "batch", None),
        ("V5 språk auto (-mc 0)", "c: språk", ra, DTW + ["-mc", "0"], "auto", "batch", None),
        ("V9 normalisert lag (-mc 0)", "sammenligning", no, DTW + ["-mc", "0"], None, "batch", None),
        ("V10 grådig dekoding (-bs 1, -mc 0)", "h: beam search velger kort sekvens", ra, DTW + ["-mc", "0", "-bs", "1"], None, "batch", None),
        ("V11 normalisert lag, grådig (-bs 1, -mc 0)", "h: sammenligning", no, DTW + ["-mc", "0", "-bs", "1"], None, "batch", None),
        ("V13 VAD foran Whisper (--vad, silero-v6.2.0, -mc 0)", "i: whisper.cpps innebygde VAD", ra, DTW + ["-mc", "0", "--vad", "-vm", str(miljo.DATA / "tmp" / "ggml-silero-v6.2.0.bin")], None, "batch", None),
        ("V14 uten tidsstempeltokens (-nt), DTW beholdt (-mc 0)", "j: -nt: whisper.cpp beholder tekst etter siste tidsstempeltoken (result_len = i + 1)", ra, DTW + ["-mc", "0", "-nt"], None, "batch", None),
        ("V15 normalisert lag uten tidsstempeltokens (-nt, -mc 0)", "j: sammenligning", no, DTW + ["-mc", "0", "-nt"], None, "batch", None),
        ("V12 0,5 s stillhet foran segmentet (-mc 0)", "f: segmentgrense uten innledning (kun diagnose)", ra, DTW + ["-mc", "0"], None, "batch_pad", None),
    ]
    rapport = {"dato": DATO, "whisper_cpp": subprocess.run(["git", "-C", str(pathlib.Path(ra.whisper_cli).parents[2]), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip(),
               "ider": ids, "referanse": {k: norm(items[k]["ref"]) for k in ids},
               "rorledningen": {k: {"for": h(a[k]), "etter": h(b[k])} for k in ids}, "varianter": {}}
    sti_rapport = HER / f"diagnose_tomt_raalag_{DATO}.json"
    if bare and sti_rapport.exists():
        rapport = json.loads(sti_rapport.read_text(encoding="utf-8"))
    for navn, hyp, lag, ekstra, sprak_valg, modus, cli in VARIANTER:
        if bare and not any(navn.startswith(b + " ") for b in bare):
            continue
        print("==", navn, flush=True)
        rapport["varianter"][navn] = {"hypotese": hyp, "per_id": {}}
        filer = [(k, w, s) for k in ids for (w, s) in wavs[k]]
        if modus == "batch_pad":  # 0,5 s digital stillhet foran hver fil (bare diagnose, ikke et tiltak)
            pad = []
            for k, w, s in filer:
                wp = w.with_name(w.stem + "_pad.wav")
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(w), "-af", "adelay=500:all=1", "-ar", "16000", "-ac", "1", str(wp)], check=True)
                pad.append((k, wp, s))
            filer = pad
        if modus == "isolert":
            grupper = [[f] for f in filer]
        else:  # én prosess per språk (batch, batch_pad) (språk er et kommandolinjeargument)
            grupper = []
            for sp in sorted({sprak_valg or items[k]["whisper_sprak"] for k, _, _ in filer}):
                grupper.append([f for f in filer if (sprak_valg or items[f[0]]["whisper_sprak"]) == sp])
        for g in grupper:
            sprak = sprak_valg or items[g[0][0]]["whisper_sprak"]
            js, err, argv = kjor(lag, [w for _, w, _ in g], sprak, ekstra, med_np=(modus != "isolert"), cli=cli)
            deb = [l for l in err.splitlines() if DEBUGLINJER.search(l)] if modus == "isolert" else []
            if modus == "isolert":
                (ARB / f"stderr_V0_{g[0][1].stem}.txt").write_text(err, encoding="utf-8")
            for (k, w, s), j in zip(g, js):
                t = tekst_fra_json(j)
                navn_fil = (w.stem.split("_", 1)[1] if "_" in w.stem else w.stem).removesuffix("_pad")
                d = {"tekst": t, "ord": len(norm(t).split()), "argv": argv, "segmenter": len(j.get("transcription", [])), "feil": j.get("feil")}
                if deb:
                    d["whisper_cpp_linjer"] = deb[:80]
                if s is not None and navn.startswith("V0 "):  # (d) cue-fiksen: tekst fra json_til_cues mot tekst i whisper.cpps JSON
                    seg = Segment("speech", s["start"], s["stopp"], "transkriber")
                    d["cuer_uten_ordtider"] = " ".join(c.tekst for c in transkriber.json_til_cues(j, seg, False))
                    d["cuer_med_ordtider"] = " ".join(c.tekst for c in transkriber.json_til_cues(j, seg, True))
                    d["varighet_s"] = round(s["stopp"] - s["start"], 2)
                rapport["varianter"][navn]["per_id"].setdefault(k, {})[navn_fil] = d
        sti_rapport.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")  # inkrementelt
    for navn, v in rapport["varianter"].items():
        for k, d in v["per_id"].items():
            ref = rapport["referanse"][k]
            hele = norm(" ".join(x["tekst"] for kk, x in d.items() if isinstance(x, dict)))
            d["_sammenslatt_wer_mot_referanse"] = round(jiwer.wer(ref, hele or ""), 3)
    sti = HER / f"diagnose_tomt_raalag_{DATO}.json"
    sti.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(sti)


if __name__ == "__main__":
    main()
