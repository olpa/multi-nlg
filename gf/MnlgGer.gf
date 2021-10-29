concrete MnlgGer of Mnlg =
  GrammarGer
  , LexiconGer
** open
  ParadigmsGer
  , (R=ResGer)
  , (T=TenseGer)
  , (I=IrregGer)
in
{
lin
  CastVtoV2 v = mkV2 (v ** { lock_V=<> });
  CastV2toV v2 = v2 ** { lock_V2=<> } ;
  CastV3toV v3 = v3 ** { lock_V3=<> } ;

  AdvAP ap adv = ap ** {s = table {aform => ap.s ! aform ++ adv.s}} ;

  MassLoi cn = DetCN (DetQuant IndefArt NumPl) cn ;

  TPasseSimple = T.TPast ;

  VPshell v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>}) accPrep zu_Prep) thema) goal ;
  VPshellDirect v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>}) datPrep accPrep) goal) thema ;

  WithIndirectClitic np vp = vp ;

  break_into_V = prefixV "ein" I.brechen_V ;
  force_V = I.zwingen_V ;
  hit_V = I.schlagen_V ;

  center_N = ParadigmsGer.mkN "Zentrum" "Zentren" neuter ;
  entrance_N = mkN "Eingang" "Eingänge" masculine ;
  knife_N = mkN  "Messer" "Messer" neuter ;
  population_N = mkN "Bevölkerung" ;
  room_N = mkN  "Zimmer" "Zimmer" neuter ;

  darxi_dakfu_CN = UseN (mkN "Stich" "Stiche" masculine) ;

  california_PN = mkPN "Kalifornien" ;
  los_angeles_PN = mkPN "Los Angeles" ;
  north_california_PN = mkPN "Nordkalifornien" ;
  san_diego_PN = mkPN "San Diego" ;
  san_jose_PN = mkPN "San Jose" ;
  san_francisco_PN = mkPN "San Francisco" ;

  commercial_A = mkA "kommerziell" ;
  cultural_A = mkA "kulturell" ;
  financial_A = mkA "finanziell" ;
  fourth_A = mkA "viert" ;

  by_Prep = mkPrep "nach" dative ;
  ins_Prep = with_Prep ;
  into_Prep = inAcc_Prep ;
  no_Prep = accPrep ;
  of_Prep = genPrep ;
}
