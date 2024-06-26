# define command
UNAME := $(shell uname)
ifeq ($(UNAME), Linux)
	LATEX := pdflatex 
	MOVE := mv 
	PDF_VIEWER := evince
	FIND := find
else ifeq ($(UNAME), Darwin)
	LATEX := $(shell which pdflatex )
	MOVE := mv 
	PDF_VIEWER := @evince -s
	FIND := find
else # Cygwin
	LATEX := $(shell which pdflatex)
	MOVE := mv 
	PDF_VIEWER := @$(shell which SumatraPDF) -reuse-instance -inverse-search "gvim --remote-silent +%l %f"
	FIND := d:\cygwin64\bin\find.exe
endif

# set output directory
OUTPUT_DIR=./intermediates/

# define flags
FLAGS+=-file-line-error
FLAGS+=-halt-on-error
FLAGS+=-output-directory=$(OUTPUT_DIR)
FLAGS+=-output-format=pdf
FLAGS+=-interaction=nonstopmode
DRAFTMODE_FLAGS=-draftmode

# define tex source file
TEX_FILES := $(shell $(FIND) ./ -maxdepth 1 -name  '*.tex')
TEX_FILES := $(notdir $(TEX_FILES))

# define target
TARGET := $(subst .tex,.pdf,$(TEX_FILES))

# define target with fullpath
TARGET_FULL_PATH := $(addprefix $(OUTPUT_DIR),$(TARGET))

all: $(TARGET_FULL_PATH) 

# %.pdf:%.tex
$(OUTPUT_DIR)%.pdf: %.tex
	@mkdir -p $(OUTPUT_DIR)
	$(LATEX) $(FLAGS) $<
ifeq ($(UNAME), Linux)
	@echo "rsync $@ ~/share/ ..."
	@rsync $@ ~/share/
	@scp $@ mianb@10.0.0.3:/d:/temp/
endif

.PHONY : tidy clean clear view debug 

tidy:
	$(MOVE) $(TARGET_FULL_PATH) ./

clean:
	$(RM) $(TARGET_FULL_PATH)
	$(RM) $(TARGET)

clear:
	$(MAKE) clean

view:
	$(PDF_VIEWER) $(TARGET) &> /dev/null &

debug:
	@echo "TARGET=$(TARGET)"
	@echo "TARGET_FULL_PATH=$(TARGET_FULL_PATH)"
	@echo "TEX_FILES=$(TEX_FILES)"
	@echo "PDF_FILE=$(PDF_FILE)"
	@echo "MAKE_FILES=$(MAKE_FILES)"
	@echo "MAKE_FILES_DIR=$(MAKE_FILES_DIR)"
