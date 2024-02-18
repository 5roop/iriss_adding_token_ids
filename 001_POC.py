import lxml.etree as ET
from pathlib import Path
from utils import save, get_present_speakers, xmlid, get_words

test_anno_path = Path("Iriss-disfl-anno-phase1/Iriss-J-Gvecg-P500001.exb.xml")
test_TEI_path = Path("iriss_with_w_and_pauses/Iriss-J-Gvecg-P500001.xml")

annodoc = ET.fromstring(test_anno_path.read_bytes())
TEI = ET.fromstring(test_TEI_path.read_bytes())
segs_to_assign_synchs = {
    w.getparent() for w in TEI.findall(".//{*}w") if ("synch" not in w.attrib.keys()) and (w.getparent().tag == "seg") 
}

for seg in segs_to_assign_synchs:
    for i, w in enumerate(seg.findall(".//{*}w")):
        seg_synch = seg.get("synch")
        if not seg_synch:
            raise Exception(f"Seg does not have synch! Seg attrib: {seg.attrib} file {input.TEI}")
        w.set("synch", seg.get("synch", "!!") + f".w{i}")
speakers = get_present_speakers(annodoc)
exbtimeline = {tli.get("id"): tli.get("time") for tli in annodoc.findall(".//tli")}
new_tier = ET.Element("tier")
new_tier.set("id", "-1")
# new_tier.set("speaker", list(speakers)[0])
new_tier.set("category", "traceability")
new_tier.set("type", "a")
words = get_words(TEI)
for speaker in speakers:
    tier = annodoc.find(f".//tier[@speaker='{speaker}']")
    for event in tier.findall("event"):
        TEI_events = [i for i in words if "#" + event.get("start") == i.get("synch")]
        if len(TEI_events) > 0:
            newevent = ET.Element(
                "event",
                **event.attrib,
            )
            event_start = event.get("start")
            event_end = event.get("end")
            top_tier_event = tier.find(
                f"event[@start='{event_start}'][@end='{event_end}']"
            )
            try:
                first_tier_content = top_tier_event.text.strip()
            except:
                first_tier_content = ""
            if first_tier_content == TEI_events[0].get("text").strip():
                addendum = ""
            else:
                addendum = " !! " + TEI_events[0].get("text").strip()
            newevent.text = TEI_events[0].get(xmlid + "id") + addendum
            new_tier.append(newevent)


list(annodoc.findall(".//{*}tier"))[-1].getparent().append(new_tier)
save(annodoc, Path("./test.exb.xml"))
