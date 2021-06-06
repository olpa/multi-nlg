concrete WrapperGer of Wrapper =
  GrammarGer
  ** open ParadigmsGer, IrregGer, Prelude, MorphoGer in {
  oper
    mkAdA : Str -> AdA ;
    mkAdA x = lin AdA (ss x) ;
  lin
    san_francisco_PN = mkPN "San Francisco" ;
    north_california_PN = mkPN "Nordkalifornien" ;
    california_PN = mkPN "Kalifornien" ;
    center_N = ParadigmsGer.mkN "Zentrum" "Zentren" neuter ;
    city_N = reg2N "Stadt" "Städte" feminine ;
    cultural_A = ParadigmsGer.mkA "kulturell" ;
    commercial_A = ParadigmsGer.mkA "kommerzielle" ;
    financial_A = ParadigmsGer.mkA "finanziell" ;
    of_Prep = genPrep ;
    populous_A = ParadigmsGer.mkA "bevölkert" ;
    fourthmost_AdA = mkAdA "viertgrößte" ;
    los_angeles_PN = mkPN "Los Angeles" ;
    san_diego_PN = mkPN "San Diego" ;
    san_jose_PN = mkPN "San Jose" ;
} ;
