cmake_minimum_required(VERSION 3.0)

if (NOT UNIX)
    message( FATAL_ERROR "This program is unix specific." )
endif ()

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

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
)

ExternalProject_Add(quine-mccluskey
    SOURCE_DIR "${CMAKE_CURRENT_LIST_DIR}/src/quine-mccluskey"
    DEPENDS exception
    INSTALL_DIR ${CMAKE_INSTALL_PREFIX}
    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
)

ExternalProject_Add(bn-to-cnf
    SOURCE_DIR "${CMAKE_CURRENT_LIST_DIR}/src/bn-to-cnf"
    DEPENDS exception quine-mccluskey
    INSTALL_DIR ${CMAKE_INSTALL_PREFIX}
    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
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

ExternalProject_Add(bnc
    SOURCE_DIR "${CMAKE_CURRENT_LIST_DIR}/src/bnc"
    DEPENDS exception quine-mccluskey bn-to-cnf bddc
    INSTALL_DIR ${CMAKE_INSTALL_PREFIX}
    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
)

ExternalProject_Add(bnmc
    SOURCE_DIR "${CMAKE_CURRENT_LIST_DIR}/src/bnmc"
    DEPENDS exception quine-mccluskey bn-to-cnf bnc
    INSTALL_DIR ${CMAKE_INSTALL_PREFIX}
    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
)
