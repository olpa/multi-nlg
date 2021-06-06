export GF_LIB_PATH=~/opt/gf-rgl/opt

# Cracks go out from the center of the shaft.
# Risse treten aus der Mitte der Welle aus.
# Grietas salen del centro del eje.
# Трещины выходят из центра вала.
# 裂纹从轴的中心散发出去。

cracks_X='(DetCN (DetQuant IndefArt NumPl) (UseN crack_N))'
shaftCenter_NP='(AdvNP (DetCN (DetQuant DefArt NumSg) (UseN center_N)) (PrepNP of_Prep (DetCN (DetQuant DefArt NumSg) (UseN shaft_N))))'
go_out_VP="(ComplSlash (VPSlashPrep (UseV go_out_V) from_spatial_Prep) ${shaftCenter_NP})"
crgoout_X="(PredVP ${cracks_X} ${go_out_VP})"

run_gf() {
  lang=$1
  echo "linearize ${crgoout_X}" | gf Wrapper.gf Wrapper${lang}.gf
}
