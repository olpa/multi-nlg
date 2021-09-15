concrete MnlgEng of Mnlg =
  GrammarEng
  , LexiconEng
** open
  ParadigmsEng
  , ResEng
in
{
lin
  CastAdvToNP adv = {
    s = table { _ => adv.s } ;
    a = agrP3 Sg ;
  } ;

  room_N = mkN "room" ;
  knife_N = mkN "knife" ;

  into_Prep = mkPrep "into" ;
}
