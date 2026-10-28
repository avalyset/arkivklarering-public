#!/usr/bin/env python3
"""Kjører inaSpeechSegmenter (INA). Kjøres av `arkivklarering.segment_inaseg` i et EGET venv (`$ARKIVKLARERING_DATA/venv-inaseg`,
`requirements-inaseg.lock`), så TensorFlow bare finnes der og det låste analysemiljøet ikke berøres. Importerer bare inaSpeechSegmenter og
standardbiblioteket.

    venv-inaseg/bin/python _inaseg_runner.py jobb.json        # batch
    venv-inaseg/bin/python _inaseg_runner.py --server         # én JSON-linje inn og én ut per fil, modellen lastes én gang

`jobb.json`: {"filer": [{"lyd": "...wav", "ut": "...json"}], "vad_engine": "smn"}. Utdata per fil: {"segmenter": [[etikett, start, stopp], ...]} med
inaSpeechSegmenters egne etiketter (speech/male/female, music, noise, noEnergy). Kartleggingen til arkivklareringens etiketter gjøres i
`arkivklarering.segment_inaseg`, ikke her. Kjønnsdeteksjon er av (den brukes ikke), så tale kommer som «speech».

Server: stdin tar {"lyd": "..."} per linje; stdout gir {"ok": true, "segmenter": [...]} eller {"ok": false, "feil": "..."} per linje. Alt annet
(TensorFlow-støy) går til stderr.
"""
import json
import os
import pathlib
import sys


def lag_segmenter(vad_engine="smn"):
    from inaSpeechSegmenter import Segmenter

    return Segmenter(vad_engine=vad_engine, detect_gender=False)


def segmenter_for(seg, lyd):
    return [[str(l), round(float(a), 4), round(float(b), 4)] for l, a, b in seg(str(lyd))]


def batch(jobb_sti):
    jobb = json.loads(pathlib.Path(jobb_sti).read_text(encoding="utf-8"))
    seg = lag_segmenter(jobb.get("vad_engine", "smn"))
    for f in jobb["filer"]:
        ut = {"segmenter": segmenter_for(seg, f["lyd"])}
        pathlib.Path(f["ut"]).write_text(json.dumps(ut, ensure_ascii=False) + "\n", encoding="utf-8")
        print("ferdig:", pathlib.Path(f["lyd"]).name, file=sys.stderr, flush=True)


def server():
    # Protokollen går på en kopi av stdout; selve fd 1 (og sys.stdout) peker til stderr, så ingen bibliotek kan forstyrre den, heller ikke fra C.
    proto = os.fdopen(os.dup(1), "w", encoding="utf-8")
    os.dup2(2, 1)
    sys.stdout = sys.stderr
    seg = lag_segmenter()
    for linje in sys.stdin:
        if not linje.strip():
            continue
        try:
            lyd = json.loads(linje)["lyd"]
            svar = {"ok": True, "segmenter": segmenter_for(seg, lyd)}
        except Exception as e:  # noqa: BLE001 (feilen sendes tilbake til kalleren)
            svar = {"ok": False, "feil": f"{type(e).__name__}: {e}"}
        proto.write(json.dumps(svar, ensure_ascii=False) + "\n")
        proto.flush()


if __name__ == "__main__":
    if sys.argv[1:] == ["--server"]:
        server()
    elif len(sys.argv) == 2:
        batch(sys.argv[1])
    else:
        raise SystemExit(__doc__)
