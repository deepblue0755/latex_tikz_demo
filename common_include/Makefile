# ANSI terminal colors
COLOR_RED    := $(shell printf '\033[31m')
COLOR_YELLOW := $(shell printf '\033[33m')
COLOR_GREEN  := $(shell printf '\033[92m')
COLOR_RESET  := $(shell printf '\033[0m')

# Check whether colored XeLaTeX Logging is available
USE_COLOR_LOG := $(shell \
	 command -v python3 >/dev/null 2>&1 && \
	 test -f buildlog.sty && \
	 test -f xelatex_color.py && \
	 echo yes)

# define command
LATEX := xelatex 
MOVE := mv 
PDF_VIEWER := evince
FIND := find

# set output directory
OUTPUT_DIR=./build

# define flags
FLAGS+=-file-line-error
FLAGS+=-halt-on-error
FLAGS+=-output-directory=$(OUTPUT_DIR)
FLAGS+=-interaction=nonstopmode
DRAFTMODE_FLAGS=-draftmode

ifeq ($(USE_COLOR_LOG), yes)
LATEX_CMD := python3 xelatex_color.py 
$(info $(COLOR_GREEN)[INFO] [Makefile] Colored XeLaTeX logging enabled$(COLOR_RESET))
else
LATEX_CMD := $(LATEX) $(FLAGS)
$(info $(COLOR_GREEN)[INFO] [Makefile] Using Plain XeLatex$(COLOR_RESET))
endif

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
	$(LATEX_CMD) $<

$(OUTPUT_DIR)/%.png: $(OUTPUT_DIR)/%.pdf
	@mkdir -p $(OUTPUT_DIR)
	@pdftoppm -png -r 600 -f 1 -l 1 $< $(basename $<)
	@mv -fv $(basename $<)-1.png $@

.PHONY : clean view share debug 

clean:
	$(RM) $(OUTPUT_DIR)/*

view:
	$(PDF_VIEWER) $(PDF_FILE) &> /dev/null &

share:
	@cp -fv $(PDF_FILE) ~/share/
	@cp -fv $(PNG_FILE) ~/share/

LIST_VAR_EXCLUDE := CURDIR MAKEFILE_LIST MAKEFLAGS MAKE_RESTARTS SHELL \
                    LIST_VAR_EXCLUDE

.PHONY: list-var

list-var:
	@$(foreach v,$(sort $(.VARIABLES)), \
	    $(if $(filter file,$(origin $(v))), \
	      $(if $(filter .% $(LIST_VAR_EXCLUDE),$(v)),,echo '$(v)';)))

print-%:
	@printf '%s = %s\n' '$*' '$($*)'
	@printf '  origin  : %s\n' '$(origin $*)'
	@printf '  literal : %s\n' '$(value $*)'

debug:
	@echo "TEX_FILE=$(TEX_FILE)"
	@echo "PDF_FILE=$(PDF_FILE)"
	@echo "PNG_FILE=$(PNG_FILE)"
	@echo "MAKE_FILES=$(MAKE_FILES)"
	@echo "MAKE_FILES_DIR=$(MAKE_FILES_DIR)"
