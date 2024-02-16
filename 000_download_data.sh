wget https://github.com/5roop/iriss_debug_and_salvage/raw/main/Iriss-disfl-anno-phase1.zip
wget https://github.com/5roop/iriss_debug_and_salvage/raw/main/iriss_with_w_and_pauses.zip

yes | unzip Iriss-disfl-anno-phase1.zip
yes | unzip iriss_with_w_and_pauses.zip

rm Iriss-disfl-anno-phase1.zip
rm iriss_with_w_and_pauses.zip

mkdir -p Iriss-disfl-anno-phase1-tokens