DIR  = $(shell cd "$( dirname "$0" )" && pwd)

SDIR = src
IDIR = include
BDIR = bin
LDIR = lib

.PHONY: wmc clean debug build install update pull

wmc: build

build:
	make -C $(SDIR)

debug:
	make -C $(SDIR) debug

install:
	make -C $(SDIR) install

lines:
	make -C $(SDIR) lines

clean:
	$(RM) -r $(LDIR)* $(IDIR) $(BDIR)
	$(MAKE) -C $(SDIR) clean

update:
	make -C $(SDIR) update

pull:
	make -C $(SDIR) pull

