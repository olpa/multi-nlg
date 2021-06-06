concrete WrapperEng of Wrapper =
  GrammarEng
  , LexiconEng
  , ConstructionEng
  , DocumentationEng --# notpresent
  , MarkupEng - [stringMark]
  , ExtendEng
  ** open ParadigmsEng, ResEng, IrregEng, Prelude, MorphoEng in {
  lin
    crack_N = mkN "crack" ;
    center_N = mkN "center" ;
    go_out_V = partV IrregEng.go_V "out" ;
    of_Prep = mkPrep "of" ;
    from_spatial_Prep = from_Prep ;
    shaft_N = mkN "shaft" ;
} ;
