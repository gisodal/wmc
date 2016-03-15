PROJECTS = exception quine-mccluskey bn-to-cnf bnc-cudd bnc bnmc-dlib bnmc
OPTIONS  = all static install
SHELL    = /bin/bash
MAKEFILE = ~/trunk/gpm/Makefile

PREFIX = $(shell cd "$( dirname "$0" )" && cd .. && pwd)

.PHONY: all clean debug build install update pull

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
	@for PROJECT in $(PROJECTS); do                     					\
		echo "REPOSITORY $${PROJECT}"; 										\
		if [ $${PROJECT} == bnc-cudd ]; then 								\
		    $(MAKE) -s -C $${PROJECT} check 2>/dev/null && 					\
			$(MAKE) -s -C $${PROJECT} $(OPTIONS);  							\
 		elif [ $${PROJECT} == bnmc ]; then 									\
			if [ "$(firstword $(OPTIONS))" == "all" ]; then 				\
				$(MAKE) -s -C $${PROJECT} dlib $(OPTIONS) || exit 1;		\
			elif [ "$(firstword $(OPTIONS))" == "debug" ]; then 			\
				$(MAKE) -s -C $${PROJECT} debug-dlib $(OPTIONS) || exit 1;	\
			else                                                			\
				$(MAKE) -s -C $${PROJECT} $(OPTIONS) || exit 1;       		\
			fi;																\
		else 																\
			$(MAKE) -s -C $${PROJECT} $(OPTIONS) || exit 1;       			\
		fi; 																\
	done

$(MAKEFILE):
	$(error $(MAKEFILE) not found..)

%/Makefile: $(MAKEFILE)
	@echo UPDATE $@
	@cp $< $@

update:
	@for PROJECT in $(PROJECTS); do                     		\
		echo "REPOSITORY $${PROJECT}"; 							\
		$(MAKE) -s $${PROJECT}/Makefile;						\
	done

pull:
	@for PROJECT in $(PROJECTS); do                     		\
		echo "REPOSITORY $${PROJECT}"; 							\
		$(MAKE) -s -C $${PROJECT} pull;							\
	done

