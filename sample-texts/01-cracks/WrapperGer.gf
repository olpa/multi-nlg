concrete WrapperGer of Wrapper =
  LangGer
  , GrammarGer
  -- , LexiconGer
  -- , ConstructionGer
  -- , DocumentationGer --# notpresent
  -- , MarkupGer - [stringMark]
  -- , ExtendGer
  ** open
    ParadigmsGer
    , IrregGer
    , Prelude
    , MorphoGer
  in
  {
  lin
    crack_N = ParadigmsGer.mkN "Riss" "Risse" masculine ;
    center_N = ParadigmsGer.mkN "Mitte" "Mitten" feminine ;
    go_out_V = ParadigmsGer.prefixV "aus" (ParadigmsGer.regV "treten") ;
    of_Prep = genPrep ;
    from_spatial_Prep = from_Prep ;
    shaft_N = ParadigmsGer.mkN "Welle" "Wellen" feminine ;
} ;
