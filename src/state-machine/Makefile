# define command
ifeq ($(shell uname), Linux)
	LATEX := pdflatex 
	MOVE := mv 
	PDF_VIEWER := evince
	FIND := find
else 
	LATEX := /cygdrive/d/texlive/2016/bin/win32/pdflatex
	MOVE := mv 
	PDF_VIEWER := /cygdrive/d/SumatraPDF-3.1.2-64/SumatraPDF
	FIND := d:\cygwin64\bin\find.exe
endif

OUTPUT_DIR=../../intermediates/

# define flags
FLAGS+=-file-line-error
FLAGS+=-halt-on-error
FLAGS+=-output-directory=$(OUTPUT_DIR)
DRAFTMODE_FLAGS=-draftmode

# define file
TEX_FILES := $(shell $(FIND) ./ -name '*.tex')
TEX_FILES := $(notdir $(TEX_FILES))

#define target
TARGET := $(subst .tex,.pdf, $(TEX_FILES))
TARGET_FULL_PATH := $(addprefix $(OUTPUT_DIR),$(TARGET))

all:$(TARGET)

%.pdf: %.tex
	$(LATEX) $(FLAGS) $<
	$(MAKE) tidy
	$(MAKE) view


.PHONY : tidy clean clear view debug 

tidy:
	$(MOVE) $(TARGET_FULL_PATH) ./

clean:
	$(RM)) -fr $(TARGET)

clear:
	$(MAKE) clean

view:
	$(PDF_VIEWER) $(TARGET)

debug:
	@echo "TEX_FILES=$(TEX_FILES)"
	@echo "TARGET=$(TARGET)"
	@echo "TARGET_FULL_PATH=$(TARGET_FULL_PATH)"
