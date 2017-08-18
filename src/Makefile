# define command
ifeq ($(shell uname), Linux)
	LATEX := pdflatex 
	MOVE := mv 
	PDF_VIEWER := evince
	FIND := find
else 
	LATEX := /cygdrive/d/texlive/2016/bin/win32/pdflatex
	MOVE := mv 
	PDF_VIEWER := /cygdrive/d/SumatraPDF/SumatraPDF
	FIND := d:\cygwin64\bin\find.exe
endif

# set output directory
OUTPUT_DIR=../intermediates/

# define flags
FLAGS+=-file-line-error
FLAGS+=-halt-on-error
FLAGS+=-output-directory=$(OUTPUT_DIR)
DRAFTMODE_FLAGS=-draftmode

# define tex source file
TEX_FILES := $(shell $(FIND) ./ -name '*.tex')

# define target
TARGET := $(subst .tex,.pdf,$(TEX_FILES))

# define Makefile
MAKE_FILES := $(shell $(FIND) ./ -name 'Makefile')
MAKE_FILES := $(filter-out ./Makefile,$(MAKE_FILES))
MAKE_FILES_DIR := $(dir $(MAKE_FILES))



all: $(TARGET)
	@for dir in $(MAKE_FILES_DIR);  do  $(MAKE) -C $$dir; done 

%.pdf: %.tex
	$(LATEX)  $(FLAGS) $<

.PHONY : tidy clean clear view debug 

clean:
	$(RM) -fr ../pdf/*.pdf

clear:
	$(MAKE) clean

view:
	$(PDF_VIEWER) $(TARGET)

debug:
	@echo "TARGET=$(TARGET)"
	@echo "TEX_FILES=$(TEX_FILES)"
	@echo "MAKE_FILES=$(MAKE_FILES)"
	@echo "MAKE_FILES_DIR=$(MAKE_FILES_DIR)"
