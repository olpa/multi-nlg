concrete WrapperSpa of Wrapper =
  GrammarSpa
  , LexiconSpa
  , ConstructionSpa
  , DocumentationSpa --# notpresent
  -- , MarkupSpa - [stringMark]
  , ExtendSpa
  ** open ParadigmsSpa, ResSpa, IrregSpa, Prelude, MorphoSpa in {
  lin
    san_francisco_PN = mkPN "San Francisco" ;
    north_california_PN = mkPN "Norte de California" ;
    california_PN = mkPN "California" ;
    center_N = mkN "centro" ;
    cultural_A = mkA "cultural" ;
    commercial_A = mkA "comercial" ;
    financial_A = mkA "financiero" ;
    of_Prep = ParadigmsSpa.mkPrep "" ParadigmsSpa.genitive ;
    populous_A = mkA "poblado" ;
    fourthmost_AdA = mkAdA "cuarto más" ;
    los_angeles_PN = mkPN "Los Angeles" ;
    san_diego_PN = mkPN "San Diego" ;
    san_jose_PN = mkPN "San José" ;
} ;
