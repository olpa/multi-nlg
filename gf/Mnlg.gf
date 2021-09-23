abstract Mnlg =
  Lang
**
{
fun
  UseV2 : V2 -> VP ;
  CastVtoV2 : V -> V2 ;
  CastV3toV : V3 -> V ;

  VPshell : V -> NP -> NP -> VP ; -- NPs: dative (becomes "to"), accusative
  VPshellDirect : V -> NP -> NP -> VP ; -- NPs: dative (becomes an object), accusative

  TPasseSimple : Tense ;

  -- i_Pron : Pron ;

  -- john_PN : PN ;

  -- break_V2: V2 ;
  -- stab_V2: V2 ;

  force_V : V;

  entrance_N : N ;
  knife_N : N ;
  room_N : N ;

  into_Prep : Prep ;
  -- to_prep : Prep ;
}
