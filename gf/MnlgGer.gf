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

  MassLoi cn = DetCN (DetQuant IndefArt NumPl) cn ;

  TPasseSimple = T.TPast ;

  VPshell v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>}) accPrep zu_Prep) thema) goal ;
  VPshellDirect v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>}) datPrep accPrep) goal) thema ;

  WithIndirectClitic np vp = vp ;

  break_into_V = prefixV "ein" I.brechen_V ;
  force_V = I.zwingen_V ;
  hit_V = I.schlagen_V ;

  center_N = ParadigmsGer.mkN "Zentrum" "Zentren" neuter ;
  entrance_N = mkN  "Eingang" "Eingänge" masculine ;
  knife_N = mkN  "Messer" "Messer" neuter ;
  room_N = mkN  "Zimmer" "Zimmer" neuter ;

  darxi_dakfu_CN = UseN (mkN "Stich" "Stiche" masculine) ;

  north_california_PN = mkPN "Nordkalifornien" ;
  san_francisco_PN = mkPN "San Francisco" ;

  commercial_A = ParadigmsGer.mkA "kommerzielle" ;
  cultural_A = ParadigmsGer.mkA "kulturell" ;
  financial_A = ParadigmsGer.mkA "finanziell" ;

  ins_Prep = with_Prep ;
  into_Prep = inAcc_Prep ;
  no_Prep = accPrep ;
  of_Prep = genPrep ;
}
