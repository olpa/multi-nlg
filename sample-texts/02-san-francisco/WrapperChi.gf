concrete WrapperChi of Wrapper =
  GrammarChi - [after_Prep]
  , LexiconChi
** open (P = ParadigmsChi) in {
  lin
    san_francisco_PN = P.mkPN "SF" ; -- 旧金山, jiùjīnshān
    north_california_PN = P.mkPN "NC" ; -- 北 加州, běi jiāzhōu
    california_PN = P.mkPN "CAL" ; -- 加利福尼亚州, jiālìfúníyà zhōu
    center_N = P.mkN "中心" ; -- zhōngxīn
    cultural_A = P.mkA "文化" ; -- wénhuà
    commercial_A = P.mkA "商业" ; -- shāngyè
    financial_A = P.mkA "金融" ; -- jīnróng
    populous_A = P.mkA "人口" ; -- rénkǒu
    fourthmost_AdA = P.mkAdA "第四" ; -- dìsì
    los_angeles_PN = P.mkPN "LA" ; -- 洛杉矶, luòshānjī
    san_diego_PN = P.mkPN "SD" ; -- 圣地亚哥, shèngdìyàgē
    san_jose_PN = P.mkPN "SJ" ; -- 圣何塞, shènghésè
    of_Prep = possess_Prep ;
    after_Prep = P.mkPrep [] "仅次于" P.mannerAdvType ;
} ;
