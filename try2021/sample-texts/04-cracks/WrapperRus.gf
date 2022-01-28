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
  lin
    crack_N = mkN "трещина" Fem Inanimate n1a ;
    center_N = mkN "центр" Masc Inanimate n1a ;
    go_out_V = mkV ParadigmsRus.perfective ParadigmsRus.transitive "выходить" "выхожу" "выходит" "4a" ;
    from_spatial_Prep = mkPrep "из" ParadigmsRus.genitive ;
    of_Prep = mkPrep "" ParadigmsRus.genitive ;
    shaft_N = mkN "вал" Masc Inanimate n1a ;
} ;
