#!/usr/bin/env python3
"""SIMULERT DEGRADERING (DEV): lager båndlyd-lignende versjoner av de 60 NB Samtale validation-segmentene (KLAR-EVAL-0003).

Kjedens rekkefølge, hver med fast parameter og fast seed (ingen tilfeldig variasjon mellom segmenter utover støyen):
  1. ujevn hastighet (wow/flutter): ffmpeg `vibrato=f=0.8:d=1.0`, målt på en 1 kHz-tone til ±1,15 % frekvensavvik, 0,8 Hz
  2. båndbegrensning 300–3400 Hz: audiomentations HighPassFilter(300 Hz) og LowPassFilter(3400 Hz), 12 dB per oktav
  3. sus: audiomentations AddGaussianSNR, 15 dB signal/støy
  4. kompresjon: audiomentations Mp3Compression (lameenc), 24 kbit/s (med tap), tilbake til 16 kHz mono wav

Kjører i et eget venv (`$ARKIVKLARERING_DATA/venv-degradering`, `requirements-degradering.lock`) slik at det låste
analysemiljøet ikke endres. Skriver `$ARKIVKLARERING_DATA/lyd/degradert/nbsamtale_validation/<id>.wav`.

    source scripts/miljo.sh && $ARKIVKLARERING_DATA/venv-degradering/bin/python eval/dev/degrader_lyd.py
"""
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import zlib

import numpy as np
import soundfile as sf
from audiomentations import AddGaussianSNR, Compose, HighPassFilter, LowPassFilter, Mp3Compression

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO))
from arkivklarering.miljo import DATA, EVAL_DATA  # noqa: E402  (bare standardbiblioteket; virker også i venv-degradering)

NBS = EVAL_DATA / "nb_samtale"
UT = DATA / "lyd" / "degradert" / "nbsamtale_validation"
SR = 16000
PARAMETRE = {"hastighet": "ffmpeg vibrato f=0.8 d=1.0 (±1,15 % frekvensavvik målt)", "bandbegrensning": "HighPassFilter 300 Hz + LowPassFilter 3400 Hz, 12 dB/oktav",
             "sus": "AddGaussianSNR 15 dB", "kompresjon": "Mp3Compression 24 kbit/s (lameenc)", "samplingsfrekvens": SR}


def kjede():
    return Compose([
        HighPassFilter(min_cutoff_freq=300, max_cutoff_freq=300, min_rolloff=12, max_rolloff=12, p=1.0),
        LowPassFilter(min_cutoff_freq=3400, max_cutoff_freq=3400, min_rolloff=12, max_rolloff=12, p=1.0),
        AddGaussianSNR(min_snr_db=15, max_snr_db=15, p=1.0),
        Mp3Compression(min_bitrate=24, max_bitrate=24, backend="lameenc", preserve_delay=True, p=1.0),
    ])


def main():
    utv = json.loads((REPO / "eval/dev/KLAR-EVAL-0003_arkivklarering_dev-utvalg_v1.0_2026-10-26.json").read_text(encoding="utf-8"))["utvalg"]
    UT.mkdir(parents=True, exist_ok=True)
    k = kjede()
    ut = {}
    for r in utv:
        id_ = f'{r["source_file_id"]}_{r["segment_id"]}'
        kilde = NBS / "valg_validation" / pathlib.PurePosixPath(r["file_name"])
        mal = UT / f"{id_}.wav"
        with tempfile.TemporaryDirectory(dir=str(UT.parent)) as tmp:
            a, b = pathlib.Path(tmp) / "a.wav", pathlib.Path(tmp) / "b.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(kilde), "-ar", str(SR), "-ac", "1", str(a)], check=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(a), "-af", "vibrato=f=0.8:d=1.0", str(b)], check=True)
            x, _ = sf.read(b, dtype="float32")
        np.random.seed(zlib.crc32(id_.encode()))  # støyen er reproduserbar per segment
        y = k(samples=x, sample_rate=SR)
        sf.write(mal, y, SR, subtype="PCM_16")
        ut[id_] = hashlib.sha256(mal.read_bytes()).hexdigest()
    (UT.parent / "degradert_nbsamtale_validation.sha256.json").write_text(json.dumps({"parametre": PARAMETRE, "sha256": ut}, indent=1) + "\n", encoding="utf-8")
    print(f"{len(ut)} segmenter degradert til {UT}")


if __name__ == "__main__":
    main()
