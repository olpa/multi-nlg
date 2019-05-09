concrete ManualEng of Manual =
  GrammarEng
  , LexiconEng
  , ConstructionEng
  , DocumentationEng --# notpresent
  , MarkupEng - [stringMark]
  , ExtendEng
  ** open ParadigmsEng, ResEng, Prelude in {
  lin
    use_V2 = mkV2 (mkV "use") ;
    usermanual_N = mkN "user manual" ;
    symbol_N = mkN "symbol" ;
} ;
