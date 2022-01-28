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
  population_N = mkN "人口" ; -- ren2 kou3
  room_N = mkN "房间";

  darxi_dakfu_CN = mkN "刀伤" "处" ; -- dao1 shang1

  california_PN = mkPN "加州" ; -- jia1 zhou1
  los_angeles_PN = mkPN "洛杉矶" ; -- luo4 shan1 ji1
  north_california_PN = mkPN "北加州" ; -- bei3 jia1 zhou1
  san_diego_PN = mkPN "圣地亚哥" ; -- sheng4 di4 ya4 ge1
  san_jose_PN = mkPN "圣荷西" ; -- sheng4 he2 xi1
  san_francisco_PN = mkPN "旧金山" ; -- jiu4 jin1 shan1

  commercial_A = mkA "商业" ; -- shang1 ye4
  cultural_A = mkA "文化" ; -- wen2 hua4
  financial_A = mkA "金融" ; -- jin1 rong2
  fourth_A = mkA "第四" ; -- di4 si4

  by_Prep = mkPrep "" ;
  ins_Prep = mkPrep "把" ;
  into_Prep = to_Prep ;
  no_Prep =  emptyPrep ;
  of_Prep = possess_Prep ;
}
