all:	dist/mnlg.pgf

export GF_LIB_PATH=../../opt/gf-rgl

dist/mnlg.pgf: $(wildcard *.gf)
	mkdir -p ./dist
	gf --make --output-dir=./dist $^
