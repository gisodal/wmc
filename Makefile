DIR  = $(shell cd "$( dirname "$0" )" && pwd)

SDIR = src
IDIR = include
BDIR = bin
LDIR = lib

.PHONY: wmc clean debug build install update pull

wmc: build

build:
	$(MAKE) -C $(SDIR)

debug:
	$(MAKE) -C $(SDIR) debug

install:
	$(MAKE) -C $(SDIR) install

lines:
	$(MAKE) -C $(SDIR) lines

clean:
	$(RM) -r $(LDIR)* $(IDIR) $(BDIR)
	$(MAKE) -C $(SDIR) clean

update:
	$(MAKE) -C $(SDIR) update

pull:
	$(MAKE) -C $(SDIR) pull

