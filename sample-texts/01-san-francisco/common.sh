export GF_LIB_PATH=~/opt/gf-rgl/opt

# en: San Francisco is the cultural, commercial, and financial center of Northern California. It is the fourth-most populous city in California, after Los Angeles, San Diego and San Jose.
# de: San Francisco ist das kulturelle, kommerzielle und finanzielle Zentrum Nordkaliforniens. Es ist die viertgrößte Stadt in Kalifornien, nach Los Angeles, San Diego und San Jose.
# es: San Francisco es el centro cultural, comercial y financiero del norte de California. Es la cuarta ciudad más poblada de California, después de Los Ángeles, San Diego y San José.
# ru: Сан-Франциско - культурный, коммерческий и финансовый центр Северной Калифорнии. Это четвертый по численности населения город в Калифорнии после Лос-Анджелеса, Сан-Диего и Сан-Хосе.
# zh: 旧金山是北加州的文化、商业和金融中心。 它是加利福尼亚州人口第四大的城市，仅次于洛杉矶，圣地亚哥和圣何塞。
# zh (PN): SF是NC的文化、商业和金融中心。 它是CAL人口第四大的城市，仅次于LA，SD和SJ。

center_ap="(ConjAP and_Conj (ConsAP (PositA cultural_A) (BaseAP (PositA commercial_A) (PositA financial_A))))"
the_center_NP="(AdvNP (DetCN (DetQuant DefArt NumSg) (AdjCN $center_ap (UseN center_N))) (PrepNP of_Prep (UsePN north_california_PN)))"
phrase_center_Cl="(PredVP (UsePN san_francisco_PN) (UseComp (CompNP $the_center_NP)))"
phrase_center_Phr="(PhrUtt NoPConj (UttS (UseCl (TTAnt TPres ASimul) PPos $phrase_center_Cl)) NoVoc)"

attributed_city_NP="(DetCN (DetQuant DefArt NumSg) (AdjCN (AdAP fourthmost_AdA (PositA populous_A)) (AdvCN (UseN city_N) (PrepNP in_Prep (UsePN california_PN)))))"
cities_ap="(ConjNP and_Conj (ConsNP (UsePN los_angeles_PN) (BaseNP (UsePN san_diego_PN) (UsePN san_jose_PN))))"
city_after_cities_NP="(ExtAdvNP $attributed_city_NP (PrepNP after_Prep $cities_ap))"
phrase_city_Cl="(PredVP (UsePron it_Pron) (UseComp (CompNP $city_after_cities_NP)))"
phrase_city_Phr="(PhrUtt NoPConj (UttS (UseCl (TTAnt TPres ASimul) PPos $phrase_city_Cl)) NoVoc)"

text="(TFullStop $phrase_center_Phr (TFullStop $phrase_city_Phr TEmpty))"
#text="$phrase_city_Phr"

run_gf() {
  lang=$1
  echo "linearize ${text}" | gf Wrapper.gf Wrapper${lang}.gf
}
