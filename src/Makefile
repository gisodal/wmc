PROJECTS = quine-mccluskey bn-to-cnf bnc-cudd bnc bnmc
OPTIONS  = all static install
SHELL    = /bin/bash

.PHONY: all clean debug build install

all:     OPTIONS = all static install
all:     build

debug:   OPTIONS = debug debug-static install
debug:   build

install: OPTIONS = install
install: build

lines:
	@for PROJECT in $(PROJECTS); do 							\
		DIRS="$${DIRS} $${PROJECT}/src $${PROJECT}/include"; 	\
	done; 														\
	find $${DIRS} -maxdepth 1 -type f | xargs wc -l;

clean:   OPTIONS = clean
clean:   build

build:
	@for PROJECT in $(PROJECTS); do                     						\
		echo -e "\n==== processing $${PROJECT} ====\n"; 						\
		if [ $${PROJECT} == bnc-cudd ]; then 									\
		    $(MAKE) -C $${PROJECT} check && $(MAKE) -C $${PROJECT} $(OPTIONS);  \
		else 																	\
			$(MAKE) -C $${PROJECT} $(OPTIONS) || exit 1;    					\
		fi; 																	\
	done

