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
  mkV2 v = ParadigmsEng.mkV2 (v ** { lock_V = <> }) ;
  TPasseSimple = TPast ;

  force_V = mkV "force" ;

  entrance_N = mkN "entrance" "entrances" ;
  knife_N = mkN "knife" "knives" ;
  room_N = mkN "room" "rooms" ;

  into_Prep = mkPrep "into" ;
}
