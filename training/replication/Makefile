MODULE_NAME = replication

subdir = training/$(MODULE_NAME)
top_builddir = ../..
include $(top_builddir)/Makefile.global

SRC_MODULE = $(MODULE_NAME).md
ALL =	$(MODULE_NAME).pdf $(MODULE_NAME).pdfpc

all:	$(ALL)

clean:
	rm -rf $(ALL)
	rm -rf $(builddir)

$(MODULE_NAME).pdf:	$(SRC_MODULE)

$(MODULE_NAME).pdfpc:	$(MODULE_NAME).pdf

.PHONY:	clean images
