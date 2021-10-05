set -u # unset variables are errors

export GF_LIB_PATH=~/nlg/opt/gf-rgl

# John broke into the room.
the_room_NP='(DetCN (DetQuant DefArt NumSg) (UseN room_N))'
break_VP="(ComplSlash (SlashV2a (CastVtoV2 break_into_V)) ${the_room_NP})"
break_Cl="(PredVP (UsePN john_PN) ${break_VP})"
break_S="(TFullStop (PhrUtt NoPConj (UttS (UseCl (TTAnt TPast ASimul) PPos ${break_Cl})) NoVoc) TEmpty)"

# I stabbed John
stab_Cl="(PredVP (UsePron i_Pron) (ComplSlash (SlashV2a stab_V2) (UsePN john_PN)))"
stab_S="(TFullStop (PhrUtt NoPConj (UttS (UseCl (TTAnt TPast ASimul) PPos ${stab_Cl})) NoVoc) TEmpty)"

# es

# Juan forzó la entrada al cuarto
into_the_room_es_PP="(PrepNP to_Prep (DetCN (DetQuant DefArt NumSg) (UseN room_N)))"
the_entrance_into_room_es_NP="(DetCN (DetQuant DefArt NumSg) (AdvCN (UseN entrance_N) ${into_the_room_es_PP}))"
break_es_VP="(ComplSlash (SlashV2a (CastVtoV2 force_V)) ${the_entrance_into_room_es_NP})"
break_es_Cl="(PredVP (UsePN john_PN) ${break_es_VP})"
break_es_S="(TFullStop (PhrUtt NoPConj (UttS (UseCl (TTAnt TPasseSimple ASimul) PPos ${break_es_Cl})) NoVoc) TEmpty)"

# Yo le di puñaladas a Juan.
give_stab_es_shell="(VPshell (CastV3toV give_V3) (UsePN john_PN) (MassLoi darxi_dakfu_CN))"
give_stab_es_VP="(WithIndirectClitic (UsePN john_PN) ${give_stab_es_shell})"
stab_es_S="(TFullStop (PhrUtt NoPConj (UttS (UseCl (TTAnt TPasseSimple ASimul) PPos (PredVP (UsePron i_Pron) ${give_stab_es_VP}))) NoVoc) TEmpty)"

# de

# Johann brach ins Zimmer ein.
into_the_room_de_NP='(PrepNP into_Prep (DetCN (DetQuant DefArt NumSg) (UseN room_N)))'
break_de_VP="(AdvVP (UseV break_into_V) ${into_the_room_de_NP})"
break_de_Cl="(PredVP (UsePN john_PN) ${break_de_VP})"
break_de_S="(TFullStop (PhrUtt NoPConj (UttS (UseCl (TTAnt TPast ASimul) PPos ${break_de_Cl})) NoVoc) TEmpty)"

# Ich stach Johann.
# same as English

# ru

# Иван ворвался в комнату.
break_into_room_ru_VP="(AdvVP (UseV break_into_V) (PrepNP into_Prep (DetCN (DetQuant DefArt NumSg) (UseN room_N))))"
break_ru_S="(TFullStop (PhrUtt NoPConj (UttS (UseCl (TTAnt TPast ASimul) PPos (PredVP (UsePN john_PN) ${break_into_room_ru_VP}))) NoVoc) TEmpty)"

# Я ударил Ивана ножом.
stab_john_ru_VP="(ComplSlash (SlashV2a (CastVtoV2 hit_V)) (UsePN john_PN))"
stab_with_knife_ru_VP="(AdvVP ${stab_john_ru_VP} (PrepNP ins_Prep (DetCN (DetQuant DefArt NumSg) (UseN knife_N))))"
stab_ru_S="(TFullStop (PhrUtt NoPConj (UttS (UseCl (TTAnt TPast ASimul) PPos (PredVP (UsePron i_Pron) ${stab_with_knife_ru_VP}))) NoVoc) TEmpty)"

#

#X="${break_de_S}"
X="${stab_S}"
Lang=Eng # Spa, Ger, ...

run_gf() {
  lang=$1
  echo "linearize ${X}"
  # echo "linearize ${X}" | gf Mnlg.gf Mnlg${lang}.gf
}

run_gf ${Lang}
