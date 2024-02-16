import lxml.etree as ET
from pathlib import Path


xmlid = "{http://www.w3.org/XML/1998/namespace}"
def save(exb: ET._Document, outpath: Path) -> None:
    ET.indent(exb, space="\t")
    exb.getroottree().write(
        outpath,
        pretty_print=True,
        encoding="utf8",
        xml_declaration='<?xml version="1.0" encoding="UTF-8"?>',
    )
    outpath.write_text(
        outpath.read_text().replace(
            "<?xml version='1.0' encoding='UTF8'?>",
            '<?xml version="1.0" encoding="UTF-8"?>',
        )
    )
def get_present_speakers(exb: ET._Document) -> set[str]:
    tiers = exb.findall(".//tier")
    return set([i.get("speaker") for i in tiers])
    