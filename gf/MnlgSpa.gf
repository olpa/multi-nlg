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
  mkV2 v = ParadigmsSpa.mkV2 (v ** { lock_V = <> });
  TPasseSimple = ExtraRomanceSpa.TPasseSimple ;

  force_V = I.forzar_V ;

  entrance_N = mkN "entrada" ;
  knife_N = mkN "cuchillo" ;
  room_N = mkN "cuarto" ;

  into_Prep = in_Prep ;
}
