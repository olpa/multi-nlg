abstract Mnlg =
  Lang
**
{
fun
  CastVtoV2 : V -> V2 ;
  CastV2toV : V2 -> V ;
  CastV3toV : V3 -> V ;
  CastAdvToNP : Adv -> NP ;

  VPshell : V -> NP -> NP -> VP ; -- NPs: dative (becomes "to"), accusative
  VPshellDirect : V -> NP -> NP -> VP ; -- NPs: dative (becomes an object), accusative

  WithIndirectClitic : NP -> VP -> VP ;

  MassLoi : CN -> NP ;

  TPasseSimple : Tense ;

  -- i_Pron : Pron ;

  -- john_PN : PN ;

  -- break_V2: V2 ;
  -- stab_V2: V2 ;

  break_into_V : V ;
  force_V : V;

  entrance_N : N ;
  knife_N : N ;
  room_N : N ;
  darxi_dakfu_N : N ;

  into_Prep : Prep ;
  -- to_prep : Prep ;
}
