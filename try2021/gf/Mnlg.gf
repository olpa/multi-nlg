abstract Mnlg =
  Lang
**
{
fun
  CastVtoV2 : V -> V2 ;
  CastV2toV : V2 -> V ;
  CastV3toV : V3 -> V ;

  VPshell : V -> NP -> NP -> VP ; -- NPs: dative (becomes "to"), accusative
  VPshellDirect : V -> NP -> NP -> VP ; -- NPs: dative (becomes an object), accusative

  WithIndirectClitic : NP -> VP -> VP ;

  MassLoi : CN -> NP ;

  TPasseSimple : Tense ;

  break_into_V : V ;
  force_V : V ;
  hit_V : V ;

  center_N : N ;
  entrance_N : N ;
  knife_N : N ;
  population_N : N ;
  room_N : N ;

  darxi_dakfu_CN : CN ;

  california_PN : PN ;
  los_angeles_PN : PN ;
  north_california_PN : PN ;
  san_diego_PN : PN ;
  san_jose_PN : PN ;
  san_francisco_PN : PN ;

  commercial_A : A ;
  cultural_A : A ;
  financial_A : A ;
  fourth_A : A ;

  by_Prep : Prep ;
  ins_Prep : Prep ;
  into_Prep : Prep ;
  no_Prep : Prep ;
  of_Prep : Prep ;
}
