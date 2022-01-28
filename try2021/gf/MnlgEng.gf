concrete MnlgEng of Mnlg =
  GrammarEng
  , LexiconEng
** open
  ParadigmsEng
  , ResEng
  , (I=IrregEng)
in
{
lin
  CastVtoV2 v = mkV2 (v ** { lock_V=<> }) ;
  CastV2toV v2 = v2 ** { lock_V2=<> } ;
  CastV3toV v3 = v3 ** { lock_V3=<> } ;

  MassLoi cn = DetCN (DetQuant IndefArt NumPl) cn ;

  TPasseSimple = TPast ;

  VPshell v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>}) noPrep toP) thema) goal ;
  VPshellDirect v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>}) noPrep noPrep) goal) thema ;

  WithIndirectClitic np vp = vp ;

  break_into_V = partV (CastV2toV break_V2) "into" ;
  force_V = mkV "force" ;
  hit_V = I.hit_V ;

  center_N = mkN "center" ;
  entrance_N = mkN "entrance" "entrances" ;
  knife_N = mkN "knife" "knives" ;
  population_N = mkN "population" ;
  room_N = mkN "room" "rooms" ;

  darxi_dakfu_CN = UseN (mkN "stab" "stabs");

  california_PN = mkPN "California" ;
  los_angeles_PN = mkPN "Los Angeles" ;
  north_california_PN = mkPN "Northern California" ;
  san_diego_PN = mkPN "San Diego" ;
  san_jose_PN = mkPN "San Jose" ;
  san_francisco_PN = mkPN "San Francisco" ;

  commercial_A = mkA "commercial" ;
  cultural_A = mkA "cultural" ;
  financial_A = mkA "financial" ;
  fourth_A = mkA "fourth" ;

  by_Prep = mkPrep "by" ;
  ins_Prep = with_Prep ;
  into_Prep = mkPrep "into" ;
  no_Prep = noPrep ;
  of_Prep = mkPrep "of" ;
}
