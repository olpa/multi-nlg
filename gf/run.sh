set -u # unset variables are errors

export GF_LIB_PATH=~/nlg/opt/gf-rgl

# John broke into the room.
into_the_room_NP='(PrepNP into_Prep (DetCN (DetQuant DefArt NumSg) (UseN room_N)))'
break_VP="(AdvVP (UseV2 break_V2) ${into_the_room_NP})"
break_Cl="(PredVP (UsePN john_PN) ${break_VP})"
break_S="(TFullStop (PhrUtt NoPConj (UttS (UseCl (TTAnt TPast ASimul) PPos ${break_Cl})) NoVoc) TEmpty)"

# I stabbed John

stab_Cl="(PredVP (UsePron i_Pron) (ComplSlash (SlashV2a stab_V2) (UsePN john_PN)))"
stab_S="(TFullStop (PhrUtt NoPConj (UttS (UseCl (TTAnt TPast ASimul) PPos ${stab_Cl})) NoVoc) TEmpty)"

# Juan forzó la entrada al cuarto
into_the_room_es_NP="(PrepNP to_Prep (DetCN (DetQuant DefArt NumSg) (UseN room_N)))"
the_entrance_es_NP="(DetCN (DetQuant DefArt NumSg) (UseN entrance_N))"
break_es_VP="(AdvVP (ComplSlash (SlashV2a (CastVtoV2 force_V)) ${the_entrance_es_NP}) ${into_the_room_es_NP})"
break_es_Cl="(PredVP (UsePN john_PN) ${break_es_VP})"
break_es_S="(TFullStop (PhrUtt NoPConj (UttS (UseCl (TTAnt TPasseSimple ASimul) PPos ${break_es_Cl})) NoVoc) TEmpty)"

# Yo le di puñaladas a Juan.
give_stab_es_shell="(VPshell (CastV3toV give_V3) (UsePN john_PN) (MassLoi (UseN darxi_dakfu_N)))"
give_stab_es_VP="(WithIndirectClitic (UsePN john_PN) ${give_stab_es_shell})"
stab_es_S="(TFullStop (PhrUtt NoPConj (UttS (UseCl (TTAnt TPasseSimple ASimul) PPos (PredVP (UsePron i_Pron) ${give_stab_es_VP}))) NoVoc) TEmpty)"

#

#X="${break_es_S}"
X="${stab_es_S}"
#Lang=Eng
Lang=Spa

run_gf() {
  lang=$1
  echo "linearize ${X}"
  # echo "linearize ${X}" | gf Mnlg.gf Mnlg${lang}.gf
}

run_gf ${Lang}
