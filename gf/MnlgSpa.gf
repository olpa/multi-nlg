concrete MnlgSpa of Mnlg =
  GrammarSpa
  , LexiconSpa
** open
  ExtraRomanceSpa
  , ParadigmsSpa
  , (I=IrregSpa)
  , ResSpa
in
{
lin
  UseV2 v2 = predV v2 ;
  CastVtoV2 v = mkV2 (v ** { lock_V = <> });
  CastV3toV v3 = v3 ** { lock_V3=<> } ;

  MassLoi cn = DetCN (DetQuant IndefArt NumPl) cn ;

  TPasseSimple = ExtraRomanceSpa.TPasseSimple ;

  VPshell v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>})) goal) thema ;
  VPshellDirect v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>})) goal) thema ;

  force_V = I.forzar_V ;

  entrance_N = mkN "entrada" ;
  knife_N = mkN "cuchillo" ;
  room_N = mkN "cuarto" ;
  darxi_dakfu_N = mkN "puñalada" ;

  into_Prep = in_Prep ;
}
