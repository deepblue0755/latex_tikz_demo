# define command
ifeq ($(shell uname), Linux)
	GNUPLOT := gnuplot 
	MOVE := mv 
	PDF_VIEWER := evince
	FIND := find
else 
	GNUPLOT := /cygdrive/d/gnuplot-5.0.5/bin/gnuplot.exe
	MOVE := mv 
	PDF_VIEWER := /cygdrive/d/SumatraPDF/SumatraPDF
	FIND := d:\cygwin64\bin\find.exe
endif

# set output directory
# OUTPUT_DIR=../../intermediates/

# define flags
# FLAGS+=-file-line-error
# FLAGS+=-halt-on-error
# FLAGS+=-output-directory=$(OUTPUT_DIR)
# DRAFTMODE_FLAGS=-draftmode

# define tex source file
PLT_FILES := $(shell $(FIND) ./ -name '*.plt')
PLT_FILES := $(notdir $(PLT_FILES))

# define target
TARGET := $(subst .plt,.pdf,$(PLT_FILES))

# define target with fullpath
TARGET_FULL_PATH := $(addprefix $(OUTPUT_DIR),$(TARGET))

all: $(TARGET) 

%.pdf:%.plt
	$(GNUPLOT) $(FLAGS) $<
	$(MAKE) view

.PHONY : tidy clean clear view debug 

tidy:
	$(MOVE) $(TARGET_FULL_PATH) ./

clean:
	$(RM) -fr $(TARGET_FULL_PATH)
	$(RM) -fr $(TARGET)

clear:
	$(MAKE) clean

view:
	$(PDF_VIEWER) $(TARGET)

debug:
	@echo "TARGET=$(TARGET)"
	@echo "PLT_FILES=$(PLT_FILES)"
	@echo "MAKE_FILES=$(MAKE_FILES)"
	@echo "MAKE_FILES_DIR=$(MAKE_FILES_DIR)"
	@echo "TARGET_FULL_PATH=$(TARGET_FULL_PATH)"
