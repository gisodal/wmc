MAKEFLAGS += --no-print-directory

DIR  = $(shell cd "$( dirname "$0" )" && pwd)

SDIR = src
IDIR = include
BDIR = bin
LDIR = lib

.PHONY: wmc clean debug build install update pull

wmc: build

build:
	@$(MAKE) -s -C $(SDIR)

debug:
	@$(MAKE) -s -C $(SDIR) debug

install:
	@$(MAKE) -s -C $(SDIR) install

lines:
	@$(MAKE) -s -C $(SDIR) lines

clean:
	@echo "RM $(LDIR)* $(IDIR) $(BDIR)"
	@$(RM) -r $(LDIR)* $(IDIR) $(BDIR)
	@$(MAKE) -s -C $(SDIR) clean

update:
	@$(MAKE) -s -C $(SDIR) update

pull:
	@$(MAKE) -s -C $(SDIR) pull

