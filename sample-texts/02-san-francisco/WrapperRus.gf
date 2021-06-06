concrete WrapperRus of Wrapper =
  GrammarRus
  , LexiconRus
  , ConstructionRus
  , DocumentationRus --# notpresent
  -- , MarkupRus - [stringMark]
  -- , ExtendRus
  ** open ParadigmsRus, ResRus, Prelude, MorphoRus, InflectionRus in {
  oper
    n1a = InflectionRus.parseIndex "1a" ;
    mkAdA : Str -> AdA ;
    mkAdA x = lin AdA (ss x) ;
  lin
    san_francisco_PN = mkPN "Сан-Франциско" ;
    north_california_PN = mkPN "Северная Калифорния" ;
    california_PN = mkPN "Калифорния" ;
    center_N = mkN "центр" Masc Inanimate n1a ;
    -- city_N = mkN "город" Masc Inanimate n1a ;
    cultural_A = mkA "культурный" ;
    commercial_A = mkA "коммерческий" ;
    financial_A = mkA "финансовый" ;
    of_Prep = mkPrep "" ParadigmsRus.genitive ;
    populous_A = mkA "населённый" ;
    fourthmost_AdA = mkAdA "четвёртый самый большой" ;
    los_angeles_PN = mkPN "Лос-Анджелес" ;
    san_diego_PN = mkPN "Сан-Диего" ;
    san_jose_PN = mkPN "Сан-Хосе" ;
} ;
