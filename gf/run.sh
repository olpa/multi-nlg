export GF_LIB_PATH=~/nlg/opt/gf-rgl

# John broke into the room.
into_the_room_NP='(PrepNP into_Prep (DetCN (DetQuant DefArt NumSg) (UseN room_N)))'
break_VP="(ComplSlash (SlashV2a break_V2) (CastAdvToNP ${into_the_room_NP}))"
break_Cl="(PredVP (UsePN john_PN) ${break_VP})"
break_S="(TFullStop (PhrUtt NoPConj (UttS (UseCl (TTAnt TPast ASimul) PPos ${break_Cl})) NoVoc) TEmpty)"

# I stabbed John

stab_Cl="(PredVP (UsePron i_Pron) (ComplSlash (SlashV2a stab_V2) (UsePN john_PN)))"
stab_S="(TFullStop (PhrUtt NoPConj (UttS (UseCl (TTAnt TPast ASimul) PPos ${stab_Cl})) NoVoc) TEmpty)"

#

X="${stab_S}"

run_gf() {
  lang=$1
  echo "to linearize: ${X}"
  echo "linearize ${X}" | gf Mnlg.gf Mnlg${lang}.gf
}

run_gf Eng
