
subdir = presentations
top_builddir = ..
include $(top_builddir)/Makefile.global

SUBDIRS = \
	plprofiler \
	storage_mvcc_issues 

all:
	for sub in $(SUBDIRS) ; do \
		$(MAKE) -C $${sub} $@ ; \
	done

clean:
	for sub in $(SUBDIRS) ; do \
		$(MAKE) -C $${sub} $@ ; \
	done

.PHONY: all clean $(SUBDIRS)
