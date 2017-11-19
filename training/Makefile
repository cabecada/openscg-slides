
subdir = training
top_builddir = ..
include $(top_builddir)/Makefile.global

SUBDIRS = \
	architecture \
	basic_sql \
	managing

all:
	for sub in $(SUBDIRS) ; do \
	    $(MAKE) -C $${sub} $@ ; \
	done
	$(MAKE) -f Makefile.courses

clean:
	for sub in $(SUBDIRS) ; do \
	    $(MAKE) -C $${sub} $@ ; \
	done
	$(MAKE) -f Makefile.courses $@

.PHONY: all clean courses $(SUBDIRS) 
