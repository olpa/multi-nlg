concrete MnlgGer of Mnlg =
  GrammarGer
  , LexiconGer
** open
  ParadigmsGer
  , (R=ResGer)
  , (T=TenseGer)
in
{
lin
  CastVtoV2 v = mkV2 (v ** { lock_V=<> });
  CastV2toV v2 = v2 ** { lock_V2=<> } ;
  CastV3toV v3 = v3 ** { lock_V3=<> } ;
  CastAdvToNP adv = {
    s = table { _ => adv.s } ;
    rc = [] ;
    ext = [] ;
    a = R.agrP3 R.Sg ;
    w = ResGer.WHeavy ;
  } ;

  MassLoi cn = DetCN (DetQuant IndefArt NumPl) cn ;

  TPasseSimple = T.TPast ;

  VPshell v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>}) accPrep zu_Prep) thema) goal ;
  VPshellDirect v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>}) datPrep accPrep) goal) thema ;

  WithIndirectClitic np vp = vp ;

  break_into_V = prefixV "ein" (irregV "brechen" "brecht" "brach" "bräche" "gebrochen") ;
  force_V = irregV "zwingen" "zwingt" "zwang" "zwänge" "gezwungen" ;

  entrance_N = mkN  "Eingang" "Eingänge" masculine ;
  knife_N = mkN  "Messer" "Messer" neuter ;
  room_N = mkN  "Zimmer" "Zimmer" neuter ;
  darxi_dakfu_N = mkN  "Stich" "Stiche" masculine ;

  into_Prep = inAcc_Prep ;
}
