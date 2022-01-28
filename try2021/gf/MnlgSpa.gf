concrete MnlgSpa of Mnlg =
  GrammarSpa
  , LexiconSpa
** open
  MorphoSpa
  , ExtraRomanceSpa
  , ParadigmsSpa
  , (I=IrregSpa)
  , (C=ConstructionSpa)
  , ResSpa
in
{
lin
  CastVtoV2 v = mkV2 (v ** { lock_V = <> });
  CastV2toV v2 = v2 ** { lock_V2=<> } ;
  CastV3toV v3 = v3 ** { lock_V3=<> } ;

  MassLoi cn = DetCN (DetQuant IndefArt NumPl) cn ;

  TPasseSimple = ExtraRomanceSpa.TPasseSimple ;

  VPshell v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>})) goal) thema ;
  VPshellDirect v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>})) goal) thema ;

  WithIndirectClitic np vp =
    let
    pron = agr2pron ! { g=np.a.g ; n=np.a.n ; p=np.a.p } ;
    clitCase = pron.s ! (CPrep P_a)
    in
    vp ** { clit2 = clitCase.c2 ++ vp.clit2 }
  ;

  break_into_V = mkV (mkV "entrar") "con fuerza" ;
  force_V = I.forzar_V ;
  hit_V = mkV "pegar" ;

  center_N = mkN "centro" ;
  entrance_N = mkN "entrada" ;
  knife_N = mkN "cuchillo" ;
  population_N = mkN "población" ;
  room_N = mkN "cuarto" ;

  darxi_dakfu_CN = UseN (mkN "puñalada") ;

  california_PN = mkPN "California" ;
  los_angeles_PN = mkPN "Los Ángeles" ;
  north_california_PN = mkPN "el Norte de California" ;
  san_diego_PN = mkPN "San Diego" ;
  san_jose_PN = mkPN "San José" ;
  san_francisco_PN = mkPN "San Francisco" ;

  commercial_A = mkA "comercial" ;
  cultural_A = mkA "cultural" ;
  financial_A = mkA "financiero" ;
  fourth_A = mkA "cuatro" ;

  by_Prep = mkPrep "por" ;
  ins_Prep = with_Prep ;
  into_Prep = in_Prep ;
  no_Prep = C.noPrep ;
  of_Prep = ParadigmsSpa.mkPrep "" ParadigmsSpa.genitive ;
}
