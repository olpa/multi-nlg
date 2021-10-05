concrete MnlgEng of Mnlg =
  GrammarEng
  , LexiconEng
** open
  ParadigmsEng
  , ResEng
  , (I=IrregEng)
in
{
lin
  CastVtoV2 v = mkV2 (v ** { lock_V=<> }) ;
  CastV2toV v2 = v2 ** { lock_V2=<> } ;
  CastV3toV v3 = v3 ** { lock_V3=<> } ;

  MassLoi cn = DetCN (DetQuant IndefArt NumPl) cn ;

  TPasseSimple = TPast ;

  VPshell v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>}) noPrep toP) thema) goal ;
  VPshellDirect v goal thema = ComplSlash (Slash2V3 (mkV3 (v ** {lock_V=<>}) noPrep noPrep) goal) thema ;

  WithIndirectClitic np vp = vp ;

  break_into_V = partV (CastV2toV break_V2) "into" ;
  force_V = mkV "force" ;
  hit_V = I.hit_V ;

  entrance_N = mkN "entrance" "entrances" ;
  knife_N = mkN "knife" "knives" ;
  room_N = mkN "room" "rooms" ;
  darxi_dakfu_CN = UseN (mkN "stab" "stabs");

  into_Prep = mkPrep "into" ;
  no_Prep = noPrep ;
  ins_Prep = with_Prep ;
}
