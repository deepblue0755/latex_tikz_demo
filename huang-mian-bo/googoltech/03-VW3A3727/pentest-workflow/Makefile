# define command
LATEX := pdflatex 
MOVE := mv 
PDF_VIEWER := evince
FIND := find

# set output directory
OUTPUT_DIR=./build

# define flags
FLAGS+=-file-line-error
FLAGS+=-halt-on-error
FLAGS+=-output-directory=$(OUTPUT_DIR)
FLAGS+=-output-format=pdf
FLAGS+=-interaction=nonstopmode
DRAFTMODE_FLAGS=-draftmode

# define tex source file
TEX_FILE := $(shell $(FIND) ./ -maxdepth 1 -name  '*.tex')
TEX_FILE := $(notdir $(TEX_FILE))
PDF_FILE := $(patsubst %.tex, %.pdf, $(TEX_FILE))
PDF_FILE := $(addprefix $(OUTPUT_DIR)/,$(PDF_FILE))
PNG_FILE := $(patsubst %.pdf, %.png, $(PDF_FILE))

all: $(PDF_FILE)  $(PNG_FILE)

# %.pdf:%.tex
$(OUTPUT_DIR)/%.pdf: %.tex
	@mkdir -p $(OUTPUT_DIR)
	$(LATEX) $(FLAGS) $<

$(OUTPUT_DIR)/%.png: $(OUTPUT_DIR)/%.pdf
	@mkdir -p $(OUTPUT_DIR)
	@pdftoppm -png -r 600 $< $(basename $<)
	@mv -fv $(basename $<)-1.png $@

.PHONY : clean view share debug 

clean:
	$(RM) $(OUTPUT_DIR)/*

view:
	$(PDF_VIEWER) $(PDF_FILE) &> /dev/null &

share:
	@cp -fv $(PDF_FILE) ~/share/
	@cp -fv $(PNG_FILE) ~/share/

debug:
	@echo "TEX_FILE=$(TEX_FILE)"
	@echo "PDF_FILE=$(PDF_FILE)"
	@echo "PNG_FILE=$(PNG_FILE)"
	@echo "MAKE_FILES=$(MAKE_FILES)"
	@echo "MAKE_FILES_DIR=$(MAKE_FILES_DIR)"
