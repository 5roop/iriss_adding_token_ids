import lxml.etree as ET
from pathlib import Path
from utils import save, get_present_speakers, xmlid, get_timeline, get_words
test_anno_path = Path("Iriss-disfl-anno-phase1/Iriss-J-Gvecg-P500001.exb.xml")
test_TEI_path = Path("iriss_with_w_and_pauses/Iriss-J-Gvecg-P500001.xml")

annodoc = ET.fromstring(test_anno_path.read_bytes())
TEI = ET.fromstring(test_TEI_path.read_bytes())
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
        TEI_events = [i for i in words if event.get("start") == i.get("start")]
        if len(TEI_events) > 0:
            newevent = ET.Element("event", **event.attrib, )
            newevent.text = TEI_events[0].get(xmlid+"id")
            new_tier.append(
                newevent
            )


list(annodoc.findall(".//{*}tier"))[-1].getparent().append(new_tier)
save(annodoc, Path("./brisi.exb.xml"))

