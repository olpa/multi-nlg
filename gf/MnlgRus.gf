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
  CastVtoV2 v = mkV2 (v ** { lock_V=<> });
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

  darxi_dakfu_CN = AdjCN (PositA (mkA "ножевой" (Z.ZA 1 Z.No Z.B_ Z.NoC))) (UseN (mkN "рана" Fem Inanimate (Z.parseIndex "1a"))) ;
  entrance_N = mkN "вход" Masc Inanimate (Z.parseIndex "1a") ;
  knife_N = mkN "нож" Masc Inanimate (Z.ZN 4 Z.No Z.B Z.NoC) ;
  room_N = mkN "комната" Fem Inanimate (Z.parseIndex "1a") ;

  into_Prep = E.to2_Prep ;
  no_Prep = E.obj_no_Prep ;
  ins_Prep = E.ins_Prep ;
}
