"""Eksport: WebVTT og segments.json.

segments.json er tidslinjen med disposisjon per segment. Musikksegmenter er merket
«foreslått klipp». Det er et forslag; ingenting klippes av verktøyet.

Formater (v0.4): WebVTT per lag, segments.json, OHMS XML (validert mot ohms.xsd), IIIF Presentation 3-manifest
(transkripsjon som merknad med motivation «supplementing», etter IIIF Cookbook 0231/0219) og MMIF (mmif-python).
Hvert format har en validator; se tests/test_eksport_formater.py.
"""
from __future__ import annotations

import json
import pathlib
from . import __version__
from . import miljo as _miljo

TALER_MERKNAD = ("Talermerkene (TALER_n) er anonyme forslag fra pyannote; ingen identifisering og ingen stemmegjenkjenning mot kjente personer. "
                "Merkene gjelder bare innenfor denne sendingen.")
FORSLAG = ("Maskinforslag til menneskelig vurdering. Ikke en klarering. "
           "Ren musikk og annet er ikke transkribert; «foreslått klipp» er ikke utført. "
           "Tale med musikk under transkriberes bare når segmenteringen merker den som tale; flagget «musikk under tale» lages bare med inaVAMOS (ADR-0019).")


def vtt_tid(s: float) -> str:
    ms = round(s * 1000)
    t, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    sek, ms = divmod(ms, 1000)
    return f"{t:02d}:{m:02d}:{sek:02d}.{ms:03d}"


def skriv_vtt(cues, sti, lag="", taler=None) -> pathlib.Path:
    """`taler`: valgfri liste (parallelt med cues) med TALER_n eller None; skrives som WebVTT voice span `<v TALER_1>tekst`."""
    sti = pathlib.Path(sti)
    linjer = [f"WEBVTT - arkivklarering v{__version__}{' - ' + lag if lag else ''}", "", f"NOTE {FORSLAG}", ""]
    if taler is not None:
        linjer[3:3] = [f"NOTE {TALER_MERKNAD}", ""]
    for i, c in enumerate(cues, 1):
        tekst = f"<v {taler[i - 1]}>{c.tekst}" if taler is not None and taler[i - 1] else c.tekst
        linjer += [str(i), f"{vtt_tid(c.start)} --> {vtt_tid(max(c.stop, c.start + 0.001))}", tekst, ""]
    sti.write_text("\n".join(linjer), encoding="utf-8")
    return sti


def skriv_segments_json(tidslinje, cues_per_lag, sti, kilde, oppsett_per_lag, flagg_per_lag=None, union_flagg=None, taler_per_lag=None, taler_info=None) -> pathlib.Path:
    """cues_per_lag: {lag: [Cue]}; oppsett_per_lag: {lag: Oppsett}; flagg_per_lag: {lag: [Flagg]} fra personvern.py."""
    sti = pathlib.Path(sti)
    segmenter = []
    for s in tidslinje:
        d = {"label": s.label, "start": round(s.start, 3), "stopp": round(s.stop, 3),
             "disposisjon": s.disposisjon}
        if s.flagg:
            d["flagg"] = s.flagg
            d["musikk_under_tale"] = [[round(a, 3), round(b, 3)] for a, b in s.musikk_under_tale]
        if s.merknad:
            d["merknad"] = s.merknad
        if s.disposisjon == "transkriber":
            # en cue hører til segmentet der midtpunktet ligger (whisper-tidskoder kan overskride kanten litt)
            d["tekst"] = {lag: [c.tekst for c in cues if s.start <= (c.start + c.stop) / 2 <= s.stop]
                          for lag, cues in cues_per_lag.items()}
            if taler_per_lag is not None:  # talermerke per cue, parallelt med «tekst» (TALER_n eller null)
                d["taler"] = {lag: [taler_per_lag[lag][i] for i, c in enumerate(cues) if s.start <= (c.start + c.stop) / 2 <= s.stop]
                              for lag, cues in cues_per_lag.items()}
            if flagg_per_lag is not None:
                d["personvern"] = {lag: [f.som_dict() for f in flagg
                                         if s.start <= (f.cue_start + f.cue_stopp) / 2 <= s.stop]
                                   for lag, flagg in flagg_per_lag.items()}
            if union_flagg is not None:
                d["personvern_union"] = [u.som_dict() for u in union_flagg if s.start <= (u.start + u.stopp) / 2 <= s.stop]
        segmenter.append(d)
    ut = {
        "versjon": __version__,
        "kilde": pathlib.Path(kilde).name,
        "merknad": FORSLAG,
        "lag": {lag: {"modell": pathlib.Path(o.modell).name, "sha256": o.sha256, "sprak": o.sprak}
                for lag, o in oppsett_per_lag.items()},
        "segmenter": segmenter,
    }
    if taler_info is not None:
        ut["talerinndeling"] = taler_info
    if flagg_per_lag is not None:
        ut["personvern"] = {"merknad": "Forslag til menneskelig vurdering; ingenting er fjernet eller endret. Et manglende flagg er ingen garanti. "
                                       "Rålaget har små bokstaver uten tegnsetting, og navnegjenkjenning forventes svakere der.",
                            "spacy": "nb_core_news_md", "bert": "NbAiLab/nb-bert-base-ner", "terskel": 0.0,
                            "union": "personvern_union per segment: samme kategori og overlappende tid slått sammen på tvers av lag; "
                                     "flagg som bare finnes i ett lag er beholdt"}
    sti.write_text(json.dumps(ut, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return sti


# ---------------------------------------------------------------- WebVTT
def valider_vtt(tekst: str) -> list[str]:
    """Leser WebVTT med webvtt-py og sjekker rekkefølge og at cuene har tekst. Det finnes ikke noe skjema for WebVTT;
    dette er en parserkontroll (W3C: https://www.w3.org/TR/webvtt1/)."""
    import io

    import webvtt

    feil = []
    try:
        v = webvtt.from_buffer(io.StringIO(tekst))
    except Exception as e:  # noqa: BLE001
        return [f"WebVTT kunne ikke leses: {e}"]
    for i, c in enumerate(v.captions, 1):
        if not c.text.strip():
            feil.append(f"cue {i} er tom")
        if c.start_in_seconds > c.end_in_seconds:
            feil.append(f"cue {i} slutter før den starter")
    return feil


# ---------------------------------------------------------------- OHMS XML
OHMS_NS = "https://www.weareavp.com/nunncenter/ohms"
OHMS_XSD = pathlib.Path(__import__("os").environ.get("ARKIVKLARERING_OHMS_XSD") or _miljo.EVAL_DATA / "ohms" / "ohms.xsd")


def _hms(sek: float) -> str:
    sek = int(round(sek))
    return f"{sek // 3600:02d}:{sek % 3600 // 60:02d}:{sek % 60:02d}"


def bygg_ohms_xml(post: dict, cues, lydfil: str, varighet_s: float, sprak: str = "nno", record_id: int = 1, taler=None) -> bytes:
    """OHMS XML (versjon 5.4 av skjemaet) fra et katalogutkast og cuene (normalisert lag). Elementene står i den
    rekkefølgen skjemaet krever. `userestrict` er 1: utkastet er ikke klarert for publisering. `sync` er tom: synkronisering
    av transkripsjonen gjøres i OHMS-applikasjonen, den lages ikke her."""
    from lxml import etree

    ns = "{%s}" % OHMS_NS
    rot = etree.Element(ns + "ROOT", nsmap={None: OHMS_NS})
    rec = etree.SubElement(rot, ns + "record", id=str(record_id), dt=datetime_dato())

    def el(navn, tekst=None, **attr):
        e = etree.SubElement(rec, ns + navn, **attr)
        if tekst is not None:
            e.text = tekst
        return e

    el("version", "5.4")
    dato = post.get("dato") or ""
    el("date", value=dato, format="yyyy-mm-dd" if len(dato) == 10 else "yyyy")
    el("title", post.get("tittel") or "(uten tittel) – utkast")
    el("duration", _hms(varighet_s))
    for ord_ in post.get("emneord", []):
        el("keyword", ord_)
    for taler in post.get("talere", []):
        el("interviewee", taler)
    el("file_name", pathlib.Path(lydfil).name)
    el("sync", "")
    el("language", sprak)
    el("user_notes", post.get("merknad", "utkast – maskinforslag"))
    idx = el("index")
    for seg in post.get("segmenter", []):
        pt = etree.SubElement(idx, ns + "point")
        etree.SubElement(pt, ns + "time").text = str(int(seg["start"]))
        etree.SubElement(pt, ns + "title").text = f"{_hms(seg['start'])} (utkast)"
        etree.SubElement(pt, ns + "synopsis").text = seg.get("sammendrag", "")
        etree.SubElement(pt, ns + "keywords").text = ";".join(seg.get("emneord", []))
        etree.SubElement(pt, ns + "subjects").text = ""
    el("description", "Utkast – maskinforslag fra arkivklarering. Ikke klarert for publisering.")
    el("transcript", "\n".join((f"{taler[i]}: " if taler is not None and taler[i] else "") + c.tekst for i, c in enumerate(cues)))
    el("rights", "Ikke klarert for publisering")
    el("fmt", "audio")
    el("userestrict", "1")
    return etree.tostring(rot, xml_declaration=True, encoding="UTF-8", pretty_print=True)


def datetime_dato() -> str:
    import datetime

    return datetime.date.today().isoformat()


def valider_ohms(xml: bytes, xsd: pathlib.Path | None = None) -> list[str]:
    """Validerer mot ohms.xsd (versjon 5.4). Tom liste = gyldig. Mangler skjemaet, reises FileNotFoundError."""
    from lxml import etree

    xsd = pathlib.Path(xsd or OHMS_XSD)
    if not xsd.is_file():
        raise FileNotFoundError(f"fant ikke OHMS-skjemaet: {xsd}")
    skjema = etree.XMLSchema(etree.parse(str(xsd)))
    doc = etree.fromstring(xml)
    return [] if skjema.validate(doc) else [str(e) for e in skjema.error_log]


def skriv_ohms_xml(sti, post, cues, lydfil, varighet_s, sprak="nno", taler=None) -> pathlib.Path:
    sti = pathlib.Path(sti)
    xml = bygg_ohms_xml(post, cues, lydfil, varighet_s, sprak, taler=taler)
    sti.write_bytes(xml)
    return sti


# ---------------------------------------------------------------- IIIF Presentation 3
def bygg_iiif_manifest(post: dict, cues_per_lag: dict, vtt_per_lag: dict, media_url: str, varighet_s: float,
                       base_url: str = "https://example.org/arkivklarering/sending", sprak: str = "no") -> dict:
    """IIIF Presentation 3-manifest for én sending, etter IIIF Cookbook 0231 (alternativ 2 og 3) og 0219: lyden som
    `painting`-annotasjon (Sound), og transkripsjonen som `supplementing`-annotasjoner på Canvasets `annotations`: én
    annotasjon per lag med hele WebVTT-fila (`Text`, `text/vtt`), og én TextualBody-annotasjon per cue med tidsfragment
    (`#t=start,slutt`). `base_url` og `media_url` er plassholdere til arkivet har egne adresser."""
    canvas = f"{base_url}/canvas/1"
    navn = {"ra": "Rålag (verbatim, utkast)", "normalisert": "Normalisert lag (utkast)"}
    sider = []
    for k, (lag, cues) in enumerate(cues_per_lag.items(), 1):
        items = [{"id": f"{base_url}/canvas/1/page/{lag}/vtt", "type": "Annotation", "motivation": "supplementing",
                  "body": {"id": vtt_per_lag[lag], "type": "Text", "format": "text/vtt",
                           "label": {"no": [f"{navn.get(lag, lag)}: WebVTT"]}, "language": sprak},
                  "target": canvas}]
        for n, c in enumerate(cues, 1):
            items.append({"id": f"{base_url}/canvas/1/page/{lag}/cue{n}", "type": "Annotation", "motivation": "supplementing",
                          "body": {"type": "TextualBody", "value": c.tekst, "format": "text/plain", "language": sprak,
                                   "label": {"no": [navn.get(lag, lag)]}},
                          "target": f"{canvas}#t={c.start:.3f},{max(c.stop, c.start + 0.001):.3f}"})
        sider.append({"id": f"{base_url}/canvas/1/page/{lag}", "type": "AnnotationPage", "items": items})
    tittel = post.get("tittel") or "(uten tittel) – utkast"
    return {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": f"{base_url}/manifest",
        "type": "Manifest",
        "label": {"no": [tittel]},
        "summary": {"no": ["Utkast – maskinforslag fra arkivklarering. Ikke klarert for publisering."]},
        "items": [{
            "id": canvas, "type": "Canvas", "duration": round(varighet_s, 3),
            "items": [{"id": f"{canvas}/page", "type": "AnnotationPage", "items": [{
                "id": f"{canvas}/page/painting", "type": "Annotation", "motivation": "painting",
                "body": {"id": media_url, "type": "Sound", "duration": round(varighet_s, 3), "format": "audio/wav"},
                "target": canvas}]}],
            "annotations": sider,
        }],
    }


def valider_iiif(manifest: dict) -> list[str]:
    """Validerer med iiif-prezi3 (pydantic-modeller for Presentation 3). Tom liste = gyldig."""
    from iiif_prezi3 import Manifest

    try:
        Manifest.model_validate(manifest)
    except Exception as e:  # noqa: BLE001
        return [str(e)]
    return []


def skriv_iiif_manifest(sti, *args, **kw) -> pathlib.Path:
    sti = pathlib.Path(sti)
    sti.write_text(json.dumps(bygg_iiif_manifest(*args, **kw), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return sti


# ---------------------------------------------------------------- MMIF
APP_BASIS = "http://apps.clams.ai/arkivklarering"  # plassholder-IRI for appene; ingen CLAMS-app er registrert


def bygg_mmif(lydfil: str, tidslinje, cues_per_lag: dict, flagg_per_lag: dict | None = None, mime: str = "audio/wav"):
    """MMIF (mmif-python) med lyddokument og én visning per komponent: segmentering (TimeFrame per segment med
    label og disposisjon), og per lag ett TextDocument per cue med cuen som TimeFrame + Alignment mot teksten.
    Personvernflagg ligger som egenskapen `flagg` på cuens
    TimeFrame (`flagg`), fordi MMIF-vokabularet ikke har en etablert type for personvernflagg."""
    from mmif import AnnotationTypes, Document, DocumentTypes, Mmif

    m = Mmif(validate=False)
    d = Document()
    d.at_type = DocumentTypes.AudioDocument
    d.id = "d1"
    d.add_property("mime", mime)
    d.location = pathlib.Path(lydfil).resolve().as_uri()
    m.add_document(d)

    v = m.new_view()
    v.metadata.app = f"{APP_BASIS}/segment/v0.4"
    v.new_contain(AnnotationTypes.TimeFrame, document="d1", timeUnit="seconds")
    for s in tidslinje:
        v.new_annotation(AnnotationTypes.TimeFrame, start=float(s.start), end=float(s.stop), label=s.label,
                         document="d1", disposisjon=s.disposisjon, flagg=list(s.flagg))
    for lag, cues in cues_per_lag.items():
        vl = m.new_view()
        vl.metadata.app = f"{APP_BASIS}/transkriber-{lag}/v0.4"
        vl.new_contain(DocumentTypes.TextDocument)
        vl.new_contain(AnnotationTypes.TimeFrame, document="d1", timeUnit="seconds")
        vl.new_contain(AnnotationTypes.Alignment)
        for c in cues:
            td = vl.new_textdocument(c.tekst, "nn")
            props = {"start": float(c.start), "end": float(c.stop), "label": "speech", "document": "d1"}
            if flagg_per_lag:
                props["flagg"] = [f.som_dict() for f in flagg_per_lag.get(lag, [])
                                  if f.cue_start is not None and abs(f.cue_start - c.start) < 1e-3 and abs(f.cue_stopp - c.stop) < 1e-3]
            tf = vl.new_annotation(AnnotationTypes.TimeFrame, **props)
            vl.new_annotation(AnnotationTypes.Alignment, source=tf.id, target=td.id)
    return m


def valider_mmif(serialisert: str) -> list[str]:
    """Leser MMIF-teksten med mmif-python, som validerer mot MMIF-skjemaet ved innlesing. Tom liste = gyldig."""
    from mmif import Mmif

    try:
        Mmif(serialisert)
    except Exception as e:  # noqa: BLE001
        return [str(e)]
    return []


def skriv_mmif(sti, *args, **kw) -> pathlib.Path:
    sti = pathlib.Path(sti)
    sti.write_text(bygg_mmif(*args, **kw).serialize(pretty=True), encoding="utf-8")
    return sti
