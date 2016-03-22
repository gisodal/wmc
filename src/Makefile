PROJECTS = exception quine-mccluskey bn-to-cnf bnc dlib bnmc
OPTIONS  = all static install
SHELL    = /bin/bash
MAKEFILE = ~/trunk/gpm/Makefile

PREFIX = $(shell cd "$( dirname "$0" )" && cd .. && pwd)

.PHONY: update

lines:
	@for PROJECT in $(PROJECTS); do 							\
		DIRS="$${DIRS} $${PROJECT}/src $${PROJECT}/include"; 	\
	done; 														\
	find $${DIRS} -maxdepth 1 -type f | xargs wc -l;


debug: OPTIONS = debug debug-static install
debug:
	@for PROJECT in $(PROJECTS); do                     	   			\
		echo "REPOSITORY $${PROJECT}"; 						   			\
        if [ $${PROJECT} == bnc-cudd ]; then 				   			\
		    $(MAKE) -s -C $${PROJECT} check 2>/dev/null && 	   			\
			$(MAKE) -s -C $${PROJECT} $(OPTIONS);  			   			\
        elif [ $${PROJECT} == bnmc ]; then 					   			\
			$(MAKE) -s -C $${PROJECT} debug-dlib $(OPTIONS) || exit 1;	\
    	else 												   			\
			$(MAKE) -s -C $${PROJECT} $@ $(OPTIONS) || exit 1;       	\
		fi;													   			\
	done;

build: OPTIONS = build static install
build:
	@for PROJECT in $(PROJECTS); do                     	   			\
		echo "REPOSITORY $${PROJECT}"; 						   			\
        if [ $${PROJECT} == bnc-cudd ]; then 				   			\
		    $(MAKE) -s -C $${PROJECT} check 2>/dev/null && 	   			\
			$(MAKE) -s -C $${PROJECT} $(OPTIONS);  			   			\
        elif [ $${PROJECT} == bnmc ]; then 					   			\
			$(MAKE) -s -C $${PROJECT} dlib $(OPTIONS) || exit 1;		\
    	else 												   			\
			$(MAKE) -s -C $${PROJECT} $@ $(OPTIONS) || exit 1;       	\
		fi;													   			\
	done;

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
				cd $${PROJECT};									\
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
		cd $${PROJECT};											\
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

