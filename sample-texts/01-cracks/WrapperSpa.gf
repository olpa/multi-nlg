concrete WrapperSpa of Wrapper =
  GrammarSpa
  , LexiconSpa
  , ConstructionSpa
  , DocumentationSpa --# notpresent
  -- , MarkupSpa - [stringMark]
  , ExtendSpa
  ** open ParadigmsSpa, ResSpa, IrregSpa, Prelude, MorphoSpa in {
  lin
    crack_N = mkN "grieta" ;
    center_N = mkN "centro" ;
    go_out_V = mkV "saler" ;
    of_Prep = ParadigmsSpa.mkPrep "" ParadigmsSpa.genitive ;
    from_spatial_Prep = from_Prep ;
    shaft_N = mkN "eje" ;
} ;
