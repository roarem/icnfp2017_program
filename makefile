TEX = latexmk -pdf --output-directory=build -file-line-error -use-make
TEXAU = latexmk --output-directory=build -file-line-error -use-make 

.PHONY: main.pdf 

all : sort_cont create_tex main.pdf view

create_tex : 
	python program.py

sort_cont :
	python sort_cont.py

copy : 
	cp sorted/sessions/* inputfiles/sessions/

view : 
	zathura main.pdf

clean : 
	rm -r build
	mkdir build

main.pdf :
	cp program/main/main.tex build/
	$(TEX) build/main.tex
	cp build/main.pdf main.pdf

