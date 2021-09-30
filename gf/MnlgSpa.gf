concrete MnlgSpa of Mnlg =
  GrammarSpa
  , LexiconSpa
** open
  MorphoSpa
  , ExtraRomanceSpa
  , ParadigmsSpa
  , (I=IrregSpa)
  , ResSpa
in
{
lin
  CastVtoV2 v = mkV2 (v ** { lock_V = <> });
  CastV2toV v2 = v2 ** { lock_V2=<> } ;
  CastV3toV v3 = v3 ** { lock_V3=<> } ;

  CastAdvToNP adv = heavyNP {
    s = table { _ => adv.s } ;
    a = agrP3 Masc Sg ;
  } ;

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

  break_into_V = mkV "entrar" ; -- not used
  force_V = I.forzar_V ;

  entrance_N = mkN "entrada" ;
  knife_N = mkN "cuchillo" ;
  room_N = mkN "cuarto" ;
  darxi_dakfu_N = mkN "puñalada" ;

  into_Prep = in_Prep ;
}
