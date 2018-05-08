cmake_minimum_required(VERSION 3.0)

if (NOT UNIX)
    message( FATAL_ERROR "This program is unix specific." )
endif ()

if (CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(CMAKE_INSTALL_PREFIX "${CMAKE_CURRENT_LIST_DIR}")
endif()

include (ExternalProject)

ExternalProject_Add(exception
    SOURCE_DIR "${CMAKE_CURRENT_LIST_DIR}/src/exception"
    INSTALL_DIR ${CMAKE_INSTALL_PREFIX}
    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
    INSTALL_COMMMAND ""
)

file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_LIST_DIR}/src/exception/include/*")
ExternalProject_Add_Step(exception forceconfigure
    COMMAND ${CMAKE_COMMAND} -E echo -n "-- Reconfigure"
    DEPENDS ${SOURCES}
    DEPENDERS configure
)

ExternalProject_Add(quine-mccluskey
    SOURCE_DIR "${CMAKE_CURRENT_LIST_DIR}/src/quine-mccluskey"
    DEPENDS exception
    INSTALL_DIR ${CMAKE_INSTALL_PREFIX}
    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
)

file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_LIST_DIR}/src/quine-mccluskey/include/*" "${CMAKE_CURRENT_LIST_DIR}/src/quine-mccluskey/src/*")
ExternalProject_Add_Step(quine-mccluskey forceconfigure
    COMMAND ${CMAKE_COMMAND} -E echo -n "-- Reconfigure"
    DEPENDS ${SOURCES}
    DEPENDERS configure
)

ExternalProject_Add(bn-to-cnf
    SOURCE_DIR "${CMAKE_CURRENT_LIST_DIR}/src/bn-to-cnf"
    DEPENDS exception quine-mccluskey
    INSTALL_DIR ${CMAKE_INSTALL_PREFIX}
    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
)

file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_LIST_DIR}/src/bn-to-cnf/include/*" "${CMAKE_CURRENT_LIST_DIR}/src/bn-to-cnf/src/*")
ExternalProject_Add_Step(bn-to-cnf forceconfigure
    COMMAND ${CMAKE_COMMAND} -E echo -n "-- Reconfigure"
    DEPENDS ${SOURCES}
    DEPENDERS configure
)

ExternalProject_Add(bddc
    SOURCE_DIR "${CMAKE_CURRENT_LIST_DIR}/src/bddc"
    INSTALL_DIR ${CMAKE_INSTALL_PREFIX}
    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
        -DCMAKE_INSTALL_INCLUDEDIR:PATH=${CMAKE_INSTALL_PREFIX}/include/bddc
        -DCMAKE_INSTALL_LIBDIR:PATH=${CMAKE_INSTALL_PREFIX}/lib
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
)

ExternalProject_Add(pseudotree
    SOURCE_DIR "${CMAKE_CURRENT_LIST_DIR}/src/pseudotree"
    DEPENDS exception quine-mccluskey bn-to-cnf
    INSTALL_DIR ${CMAKE_INSTALL_PREFIX}
    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
)

file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_LIST_DIR}/src/pseudotree/include/*" "${CMAKE_CURRENT_LIST_DIR}/src/pseudotree/source/*")
ExternalProject_Add_Step(pseudotree forceconfigure
    COMMAND ${CMAKE_COMMAND} -E echo -n "-- Reconfigure"
    DEPENDS ${SOURCES}
    DEPENDERS configure
)

ExternalProject_Add(bnc
    SOURCE_DIR "${CMAKE_CURRENT_LIST_DIR}/src/bnc"
    DEPENDS exception quine-mccluskey bn-to-cnf bddc
    INSTALL_DIR ${CMAKE_INSTALL_PREFIX}
    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
)

file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_LIST_DIR}/src/bnc/include/*" "${CMAKE_CURRENT_LIST_DIR}/src/bnc/src/*")
ExternalProject_Add_Step(bnc forceconfigure
    COMMAND ${CMAKE_COMMAND} -E echo -n "-- Reconfigure"
    DEPENDS ${SOURCES}
    DEPENDERS configure
)

ExternalProject_Add(bnmc
    SOURCE_DIR "${CMAKE_CURRENT_LIST_DIR}/src/bnmc"
    DEPENDS exception quine-mccluskey bn-to-cnf bnc
    INSTALL_DIR ${CMAKE_INSTALL_PREFIX}
    UPDATE_COMMAND ""
    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
)

file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_LIST_DIR}/src/bnmc/include/*" "${CMAKE_CURRENT_LIST_DIR}/src/bnmc/src/*")
ExternalProject_Add_Step(bnmc forceconfigure
    COMMAND ${CMAKE_COMMAND} -E echo -n "-- Reconfigure"
    DEPENDS ${SOURCES}
    DEPENDERS configure
)

