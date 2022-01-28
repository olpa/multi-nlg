all:	dist/mnlg.pgf

clean:
	rm x.sh x.treebank

export GF_LIB_PATH=${HOME}/opt/gf-rgl/dist

dist/mnlg.pgf: $(wildcard *.gf)
	mkdir -p ./dist
	gf --make --output-dir=./dist $^

test-bank: x.treebank treebank_from_tests.txt
	diff $^

x.treebank: dist/mnlg.pgf x.sh
	sh x.sh | grep -v -e '^This is GF version' -e '^Built on' > x.treebank

x.sh: mk_script_treebank_from_tests.py
	python3 $< >x.sh
