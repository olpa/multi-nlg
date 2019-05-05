abstract Matrix = Lang, Extend ** {
  flags
    startcat = Text ;
  fun
    timeunitNP : Card -> Timeunit -> NP ; -- three hours
    Range : Card -> Card -> Adv ;
    SSubjS' : S -> Subj -> S -> S ;
    timeHourMinute' : Hour -> Card -> Adv ; -- at six forty
    monthDayNP : Month -> Numeral -> NP ; -- June third
  fun
    -- A
    obvious_A : A ;
    happy_A : A ;
    open_A : A ;
    soft_A : A ;
    -- Adv
    every_day_Adv : Adv ;
    nearly_Adv : Adv ;
    -- Conj
    whether_Conj : Conj ;
    -- PN
    abrams_PN : PN ;
    browne_PN : PN ;
    -- N
    cigarette_N : N ;
    idea_N : N ;
    morning_N : N ;
    picture_N : N ;
    tobacco_N : N ;
    way_N : N ;
    -- V
    arrive_V : V ;
    bark_V : V ;
    open_V : V ;
    wonder_V : V ;
    -- V2
    arrive_V2 : V2 ;
    bother_V2 : V2 ;
    chase_V2 : V2 ;
    give_V2 : V2 ;
    squeeze_in_V2 : V2 ;
    try_V2 : V2 ;
    -- V3
    bet_V3 : V3 ;
    hand_V3 : V3 ;
    hand_to_V3 : V3 ;
    leave_V3 : V3 ;
    put_in_V3 : V3 ;
    take_V3 : V3 ;
    -- VV
    intend_VV : VV ;
    keep_VV : VV ;
    seem_VV : VV ;
    go_VV   : VV ;
    -- V2A
    consider_V2A : V2A ;
    strike_V2A : V2A ;
    wipe_V2A : V2A ;
    -- V2S
    bet_V2S : V2S ;
    bother_V2S : V2S ;
    -- V2V
    believe_V2V : V2V ;
    intend_V2V : V2V ;
    promise_V2V : V2V ;

} ;
