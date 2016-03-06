DIR  = $(shell cd "$( dirname "$0" )" && pwd)

SDIR = src
IDIR = include
BDIR = bin
LDIR = lib

.PHONY: all clean debug build install

all: build

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

