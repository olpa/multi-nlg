concrete MnlgRus of Mnlg =
  GrammarRus
  , LexiconRus
** open
  Prelude
  , ParadigmsRus
  , ResRus
  , (Z=InflectionRus)
  , (E=ExtraRus)
in
{
lin
  CastVtoV2 v = mkV2 (v ** { lock_V=<> }) ;
  CastV2toV v2 = v2 ** { lock_V2=<> } ;
  CastV3toV v3 = v3 ** { lock_V3=<> } ;

  MassLoi cn = DetCN (DetQuant IndefArt NumPl) cn ;

  TPasseSimple = TPast ;

  VPshellDirect v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>}) E.obj_no_Prep E.to_dat_Prep) thema) goal ;
  VPshell v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>}) E.to_dat_Prep E.obj_no_Prep) goal) thema ;

  WithIndirectClitic np vp = vp ;

  break_into_V = mkV perfective transitive "ворваться" "ворвусь" "ворвётся" "6°b/c";
  force_V = mkV perfective transitive "заставить" "заставлю" "заставит" "4a" ;
  hit_V = mkV perfective transitive "ударить" "ударю" "ударит" "4a" ;

  center_N = mkN "центр" Masc Inanimate (Z.parseIndex "1a") ;
  entrance_N = mkN "вход" Masc Inanimate (Z.parseIndex "1a") ;
  knife_N = mkN "нож" Masc Inanimate (Z.ZN 4 Z.No Z.B Z.NoC) ;
  population_N = mkN "население" Neut Inanimate (Z.parseIndex "7a") ;
  room_N = mkN "комната" Fem Inanimate (Z.parseIndex "1a") ;

  darxi_dakfu_CN = AdjCN (PositA (mkA "ножевой" (Z.ZA 1 Z.No Z.B_ Z.NoC))) (UseN (mkN "рана" Fem Inanimate (Z.parseIndex "1a"))) ;

  california_PN = mkPN "Калифорния" feminine inanimate ;
  los_angeles_PN = mkPN "Лос-Анджелес" masculine inanimate ;
  north_california_PN =
    let north_A : A = mkA "Северный" (Z.parseAdjIndex "1*a") in
    mkCompoundN (makeNFFromAF north_A feminine inanimate) " " california_PN ;
  san_diego_PN = mkPN "Сан-Диего" masculine inanimate Z.ZN0 ;
  san_jose_PN = mkPN "Сан-Хосе" masculine inanimate Z.ZN0 ;
  san_francisco_PN = mkPN "Сан-Франциско" masculine inanimate ;

  commercial_A = mkA "коммерческий" ;
  cultural_A = mkA "культурный" ;
  financial_A = mkA "финансовый" ;
  fourth_A = mkA "четвёртый" ;

  by_Prep = mkPrep "по" ParadigmsRus.dative ;
  ins_Prep = E.ins_Prep ;
  into_Prep = E.to2_Prep ;
  no_Prep = E.obj_no_Prep ;
  of_Prep = mkPrep "" ParadigmsRus.genitive ;
}
