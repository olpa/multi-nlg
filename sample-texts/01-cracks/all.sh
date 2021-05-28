source common.sh

echo "linearize ${crgoout_X}" | gf Wrapper.gf \
  WrapperEng.gf \
  WrapperGer.gf \
  WrapperSpa.gf \
  WrapperRus.gf \
  WrapperChi.gf

