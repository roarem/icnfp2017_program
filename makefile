TEX = latexmk -pdf --output-directory=build -file-line-error -use-make
TEXAU = latexmk --output-directory=build -file-line-error -use-make 

.PHONY: main.pdf 

all : sort tex pdf view

tex : 
	python tex.py

sort :
	python sort.py

view : 
	zathura main.pdf

clean : 
	rm -r build
	mkdir build

pdf :
	cp program/main/main.tex build/
	$(TEX) build/main.tex
	cp build/main.pdf main.pdf

