:: pdflatex -file-line-error -halt-on-error -output-directory=./output ./junction-diagram.tex
::pdflatex -file-line-error -halt-on-error -output-directory=./output ./geogebra-export.tex
set TEX_SRC_FILE=.\bar-chart.tex
set PDFLATEX=D:\texlive\2016\bin\win32\pdflatex.exe
%PDFLATEX% -file-line-error -halt-on-error -output-directory=./output %TEX_SRC_FILE%


@PAUSE
