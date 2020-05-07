PANDOC = pandoc
OUTPUT = build
INPUT  = README-source
BIB    = README.bib

.PHONY: README.pdf


FLAGS = \
	-F pandoc-crossref \
	-f markdown \
	--pdf-engine=pdflatex \
	--filter=pandoc-citeproc \
	--filter=pandoc/bin/includes.hs \
	--bibliography=$(BIB) \
	--csl=pandoc/bibliography.csl \
	-s

#	--filter=pandoc/bin/table-filter.py \



FLAGS_TEX =
	--bibliography=$(BIB) \
	--csl=pandoc/bibliography.csl \
	-s \
	-F pandoc-crossref

FLAGS_PDF = --template=pandoc/template.latex

all: README.pdf

mkdir:
	@if [ ! -e build ]; then mkdir build; fi

pdf: mkdir
	$(PANDOC) -o $(OUTPUT)/README.pdf $(FLAGS) $(FLAGS_PDF) README.yaml README-source.md

clean:
	rm -f build/README.pdf
