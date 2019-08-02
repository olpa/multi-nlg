concrete ManualEng of Manual =
  GrammarEng
  , LexiconEng
  -- , ConstructionEng
  , DocumentationEng --# notpresent
  , MarkupEng - [stringMark]
  , ExtendEng
  ** open ParadigmsEng, ResEng, IrregEng, Prelude, MorphoEng in {
  lin
    use_V2 = mkV2 (mkV "use") ;
    help_V2 = mkV2 (mkV "help") ;
    usermanual_N = mkN "user manual" ;
    symbol_N = mkN "symbol" ;
    sign_N = mkN "sign" ;
    crack_N = mkN "crack" ;
    center_N = mkN "center" ;
    go_out_V = partV IrregEng.go_V "out" ;
    of_Prep = mkPrep "of" ;
    at_Prep = mkPrep "at" ;
    shaft_N = mkN "shaft" ;
    each_Det = mkDeterminer singular "each";
    engine_N = mkN "engine" ;
    generator_N = mkN "generator" ;
    csd_N = mkN "CSD" ;
    operate_V2 = mkV2 (mkV "operate") ;
    speed_N = mkN "speed" ;
    AC_N = mkN "AC" ;
    constant_A = mkA "constant" ;
    rpm_N = mkN "rpm" ;

} ;







