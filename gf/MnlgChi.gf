concrete MnlgChi of Mnlg =
  GrammarChi
  , LexiconChi-[stab_V2]
** open
  Prelude
  , ParadigmsChi
  , ResChi
  , (T=TenseChi)
in
{
lin
  CastVtoV2 v = mkV2 (v ** { lock_V=<> });
  CastV2toV v2 = v2 ** { lock_V2=<> } ;
  CastV3toV v3 = v3 ** { lock_V3=<> } ;

  MassLoi cn = DetCN (DetQuant IndefArt NumPl) cn ;

  TPasseSimple = T.TPast ;

  VPshellDirect v goal thema = insertObj goal (insertObj thema (UseV v)) ;
  VPshell = VPshellDirect ;

  WithIndirectClitic np vp = vp ;

  break_into_V = mkV "闯进" ; -- chuang3 jin4
  force_V = mkV "迫使" ; -- po4 shi3
  hit_V = mkV "击" ; -- ji1
  stab_V2 = mkV2 "刺伤" ; -- ci4 shang1

  center_N = mkN "中心" ; -- zhong1 xin1
  entrance_N = mkN "入口" ;
  knife_N = mkN "刀" "把" ;
  room_N = mkN "房间";

  darxi_dakfu_CN = mkN "刀伤" "处" ; -- dao1 shang1

  san_francisco_PN = mkPN "旧金山" ; -- jiu4 jin1 shan1
  north_california_PN = mkPN "北 加州" ; --  bei3 jia1 zhou1

  commercial_A = mkA "商业" ; -- shang1 ye4
  cultural_A = mkA "文化" ; -- wen2 hua4
  financial_A = mkA "金融" ; -- jin1 rong2

  ins_Prep = mkPrep "把" ;
  into_Prep = to_Prep ;
  no_Prep =  emptyPrep ;
  of_Prep = possess_Prep ;
}
