concrete MatrixEng of Matrix =
  GrammarEng
  , LexiconEng
  , ConstructionEng
  , DocumentationEng --# notpresent
  , MarkupEng - [stringMark]
  , ExtendEng
  ** open ParadigmsEng, ResEng, (R = ResEng), (S = SyntaxEng), (Sy = SymbolicEng), Prelude in {
  lin
    timeunitNP n time = S.mkNP n time ;
    Range n m = {
      s = "from" ++  n.s ! False ! Nom ++ "to" ++  m.s ! False ! Nom
      } ;
    SSubjS' a s b = {s = a.s ++ s.s ++ b.s} ;
    timeHourMinute' h m = let
      min = m.s ! True ! R.Nom
      in
      S.mkAdv at_Prep (Sy.symb (h.s ++ min)) ;
    monthDayNP m d = let
      month : NP = S.mkNP m
      in month ** {s =\\c => month.s ! c ++ d.s ! True ! NOrd ! Nom} ;

  lin
    -- A
    obvious_A = mkA "obvious" ;
    happy_A = mkA "happy" ;
    open_A = mkA "open" ;
    soft_A = mkA "soft" ;
    -- Adv
    every_day_Adv = mkAdv "every day" ;
    nearly_Adv = mkAdv "nearly" ;
    -- Conj
    whether_Conj = mkConj "whether" ;
    -- PN
    abrams_PN = mkPN (mkN masculine (mkN "Abrams")) ;
    browne_PN = mkPN (mkN masculine (mkN "Browne")) ;
    -- N
    cigarette_N = mkN "cigarette" ;
    idea_N = mkN "idea" ;
    morning_N = mkN "morning" ;
    picture_N = mkN "picture" ;
    tobacco_N = mkN "tobacco" ;
    way_N = mkN "way" ;
    -- V
    arrive_V = mkV "arrive" ;
    bark_V = mkV "bark" ;
    open_V = mkV "open" "opened" ;
    wonder_V = mkV "wonder" ;
    -- V2
    arrive_V2 = mkV2 arrive_V on_Prep ;
    bother_V2 = mkV2 "bother" ;
    chase_V2 = mkV2 "chase" ;
    give_V2 = mkV2 "give" ;
    squeeze_in_V2 = mkV2 (partV (mkV "squeeze") "in") ;
    try_V2 = mkV2 (mkV "try") to_Prep ;
    -- V3
    bet_V3 = mkV3 (mkV "bet" "bet" "bet") ;
    hand_V3 = mkV3 (mkV "hand") ;
    hand_to_V3 = mkV3 (mkV "hand") to_Prep ;
    leave_V3 = mkV3 (mkV "leave" "left" "left") noPrep to_Prep ;
    put_in_V3 = mkV3 (mkV "put" "put" "put") in_Prep ;
    take_V3 = mkV3 (mkV "take" "took" "taken") ;
    -- VV
    intend_VV = mkVV intend_V ;
    keep_VV = ingVV (mkV "keep" "kept" "kept") ;
    seem_VV = mkVV (mkV "seem") ;
    go_VV   = mkVV (mkV "go") ;
    -- V2A
    consider_V2A = mkV2A (mkV "consider") ;
    strike_V2A = mkV2A (mkV "strike") noPrep (mkPrep "as") ;
    wipe_V2A = mkV2A (mkV "wipe") noPrep ;
    -- V2S
    bet_V2S = mkV2S (mkV "bet" "bet" "bet") noPrep ;
    bother_V2S = mkV2S (mkV "bother") noPrep ;
    -- V2V
    believe_V2V = mkV2V (mkV "believe") noPrep to_Prep ;
    intend_V2V = mkV2V intend_V noPrep to_Prep ;
    promise_V2V = mkV2V (mkV "promise") noPrep to_Prep ;

  oper
    intend_V : V ;
    intend_V = mkV "intend" ;

} ;
