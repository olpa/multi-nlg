concrete MnlgEng of Mnlg =
  GrammarEng
  , LexiconEng
** open
  ParadigmsEng
  , ResEng
in
{
lin
  UseV2 v2 = predV v2 ;
  CastVtoV2 v = mkV2 (v ** { lock_V=<> }) ;
  CastV3toV v3 = v3 ** { lock_V3=<> } ;

  TPasseSimple = TPast ;

  VPshell v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>}) noPrep toP) thema) goal ;
  VPshellDirect v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>}) noPrep noPrep) goal) thema ;

  force_V = mkV "force" ;

  entrance_N = mkN "entrance" "entrances" ;
  knife_N = mkN "knife" "knives" ;
  room_N = mkN "room" "rooms" ;

  into_Prep = mkPrep "into" ;
}
