PROJECTS = exception quine-mccluskey bn-to-cnf bnc dlib bnmc
OPTIONS  = all static install
SHELL    = /bin/bash
MAKEFILE = ~/trunk/gpm/Makefile

PREFIX = $(shell cd "$( dirname "$0" )" && cd .. && pwd)

.PHONY: all build debug reset update lines

all: build

build: OPTIONS = build static install
build:
	@for PROJECT in $(PROJECTS); do     						\
		echo "REPOSITORY $${PROJECT}"; 							\
		$(MAKE) -s -C $${PROJECT} $(OPTIONS) || exit 1;			\
	done

debug: OPTIONS = debug debug-static install
debug:
	@for PROJECT in $(PROJECTS); do     						\
		echo "REPOSITORY $${PROJECT}"; 							\
		$(MAKE) -s -C $${PROJECT} $(OPTIONS) || exit 1;			\
	done

lines:
	@for PROJECT in $(PROJECTS); do 							\
		DIRS="$${DIRS} $${PROJECT}/src $${PROJECT}/include"; 	\
	done; 														\
	find $${DIRS} -maxdepth 1 -type f | xargs wc -l;


$(MAKEFILE):
	$(error $(MAKEFILE) not found..)

%/Makefile: | $(MAKEFILE)
	@echo UPDATE $@;
	@cp $< $@;

update:
	@if [ -f $(MAKEFILE) ]; then 								\
		for PROJECT in $(PROJECTS); do     						\
			echo "REPOSITORY $${PROJECT}"; 						\
			cmp -s $${PROJECT}/Makefile $(MAKEFILE);   			\
			if [ $$? -ne 0 ]; then 								\
				cd $${PROJECT} || continue;						\
				echo "UPDATE Makefile";							\
				cp $(MAKEFILE) Makefile; 						\
				cd ..; 											\
			fi;													\
		done; 													\
	else 														\
		echo "$(MAKEFILE) does not exist"; 						\
		exit 1; 												\
	fi;

reset:
	@for PROJECT in $(PROJECTS); do     						\
		echo "REPOSITORY $${PROJECT}"; 							\
		cd $${PROJECT} || continue;								\
		if [ "$$(git diff --name-only Makefile)" != "" ]; then 	\
			echo RESET Makefile;								\
			git checkout Makefile;								\
		fi; 													\
		cd ..;													\
	done

%:
	@for PROJECT in $(PROJECTS); do     						\
		echo "REPOSITORY $${PROJECT}"; 							\
		$(MAKE) -s -C $${PROJECT} $@ || exit 1;					\
	done

