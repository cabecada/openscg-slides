
subdir = .
top_builddir = .
include $(top_builddir)/Makefile.global

SUBDIRS = \
	training \
	presentations

all:
	for sub in $(SUBDIRS) ; do \
		$(MAKE) -C $${sub} $@ ; \
	done

clean:
	for sub in $(SUBDIRS) ; do \
		$(MAKE) -C $${sub} $@ ; \
	done

.PHONY: all clean $(SUBDIRS)
