TEX_FILE := remember-take-vd-iron.tex
OUTPUT_DIR := ./build
PDF_FILE := $(patsubst %.tex, %.pdf, $(TEX_FILE))
PDF_FILE := $(addprefix $(OUTPUT_DIR)/,$(PDF_FILE))

all:$(PDF_FILE)

$(OUTPUT_DIR)/%.pdf: %.tex
	@mkdir -p $(OUTPUT_DIR)
	pdflatex -output-directory=$(OUTPUT_DIR) $<

.PHONEY: clean debug share
clean:
	$(RM) $(OUTPUT_DIR)/*
debug:
	@echo $(PDF_FILE)
share:
	@cp -fv $(PDF_FILE) ~/share/
