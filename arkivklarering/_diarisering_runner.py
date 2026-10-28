#!/usr/bin/env python3
"""Kjører pyannote-talerinndeling. Kjøres av `arkivklarering.diarisering` i et EGET venv (`$ARKIVKLARERING_DATA/venv-diarisering`,
`requirements-diarisering.lock`), så det låste analysemiljøet ikke berøres. Importerer bare pyannote og standardbiblioteket.

    venv-diarisering/bin/python _diarisering_runner.py jobb.json

`jobb.json`: {"filer": [{"lyd": "...wav", "ut": "...json"}], "modell": "pyannote/speaker-diarization-community-1", "enhet": "cpu",
"antall_talere": null}. Modellen lastes én gang. Utdata per fil: {"modell", "tur": [{"start", "stopp", "etikett"}], "tur_med_overlapp": [...]}
der `tur` er pyannotes ikke-overlappende inndeling (`exclusive_speaker_diarization`, den WhisperX bruker for å tildele ord til talere) og
`tur_med_overlapp` er den fulle inndelingen. Etikettene er pyannotes (SPEAKER_00 …); navnene TALER_n settes av `arkivklarering.diarisering`.

Hugging Face-tokenet (modellen er gated) leses her, i prosessen, fra miljøvariabelen HF_TOKEN eller fra `.env` i repoet. Det skrives aldri ut,
logges ikke og sendes ikke som kommandolinjeargument.
"""
import json
import os
import pathlib
import re
import sys


def les_token():
    t = os.environ.get("HF_TOKEN")
    if t:
        return t
    env = pathlib.Path(__file__).resolve().parent.parent / ".env"
    if env.is_file():
        m = re.search(r"^\s*HF_TOKEN\s*=\s*['\"]?([^\s'\"]+)", env.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1)
    raise SystemExit("HF_TOKEN mangler (miljøet eller .env). Modellen er gated på Hugging Face.")


def main(jobb_sti):
    jobb = json.loads(pathlib.Path(jobb_sti).read_text(encoding="utf-8"))
    import torch
    from pyannote.audio import Pipeline

    pipe = Pipeline.from_pretrained(jobb["modell"], token=les_token())
    if pipe is None:
        raise SystemExit(f"fikk ikke lastet {jobb['modell']} (mangler tilgang?)")
    pipe.to(torch.device(jobb.get("enhet", "cpu")))
    for f in jobb["filer"]:
        kw = {}
        if jobb.get("antall_talere"):
            kw["num_speakers"] = int(jobb["antall_talere"])
        ut = pipe(f["lyd"], **kw)
        full = getattr(ut, "speaker_diarization", ut)
        excl = getattr(ut, "exclusive_speaker_diarization", full)
        tur = lambda a: [{"start": round(t.start, 3), "stopp": round(t.end, 3), "etikett": str(l)} for t, _, l in a.itertracks(yield_label=True)]  # noqa: E731
        pathlib.Path(f["ut"]).write_text(json.dumps({"modell": jobb["modell"], "tur": tur(excl), "tur_med_overlapp": tur(full)}, ensure_ascii=False) + "\n", encoding="utf-8")
        print("ferdig:", pathlib.Path(f["lyd"]).name, flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
