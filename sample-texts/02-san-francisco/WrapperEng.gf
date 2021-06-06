concrete WrapperEng of Wrapper =
  GrammarEng
  , LexiconEng
  , ConstructionEng
  , DocumentationEng --# notpresent
  , MarkupEng - [stringMark]
  , ExtendEng
  ** open ParadigmsEng, ResEng, IrregEng, Prelude, MorphoEng in {
  lin
    san_francisco_PN = mkPN "San Francisco" ;
    north_california_PN = mkPN "Northern California" ;
    california_PN = mkPN "California" ;
    center_N = mkN "center" ;
    cultural_A = mkA "cultural" ;
    commercial_A = mkA "commercial" ;
    financial_A = mkA "financial" ;
    of_Prep = mkPrep "of" ;
    populous_A = mkA "populous" ;
    fourthmost_AdA = mkAdA "fourth-most" ;
    los_angeles_PN = mkPN "Los Angeles" ;
    san_diego_PN = mkPN "San Diego" ;
    san_jose_PN = mkPN "San Jose" ;
} ;
