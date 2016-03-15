MAKEFLAGS += --no-print-directory

DIR  = $(shell cd "$( dirname "$0" )" && pwd)

SDIR = src
IDIR = include
BDIR = bin
LDIR = lib

.PHONY: wmc clean

wmc: build

clean:
	@echo "RM $(LDIR)* $(IDIR) $(BDIR)"
	@$(RM) -r $(LDIR)* $(IDIR) $(BDIR)
	@$(MAKE) -s -C $(SDIR) clean

%:
	@$(MAKE) -s -C $(SDIR) $@

