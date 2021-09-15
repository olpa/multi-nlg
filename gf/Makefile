all:	dist/mnlg.pgf

dist/mnlg.pgf: $(wildcard *.gf)
	mkdir -p ./dist
	gf --make --output-dir=./dist $^
