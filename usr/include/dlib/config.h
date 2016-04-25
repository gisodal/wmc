#ifndef DLIB_CONFIG_H
#define DLIB_CONFIG_H

// this condig file is made with the aid of the documentation that can be found
// at dlib.net/compile.html.

// #define ENABLE_ASSERTS

/*
    Defining this directive causes all the DLIB_ASSERT macros to be active. If
    you are using Visual Studio or CMake then ENABLE_ASSERTS will be
    automatically enabled for you when you compile in debug mode. However, if
    you are using a different build system then you might have to manually
    enable it if you want to turn the asserts on.
*/

#define DLIB_ISO_CPP_ONLY

/*
    This is a #define directive that you can set to cause the library to exclude
    all non ISO C++ code (The things in the API wrappers section and any objects
    that depend on those wrappers). This is useful if you are trying to build on
    a system that isn't fully supported by the library or if you just decide you
    don't want any of that stuff compiled into your program for your own
    reasons.
*/

#define DLIB_NO_GUI_SUPPORT

/*
    This is just like the DLIB_ISO_CPP_ONLY option except that it excludes only
    the GUI part of the library. An example of when you might want to use this
    would be if you don't need GUI support and you are building on a UNIX
    platform that doesn't have the X11 headers installed.
*/

// #define NO_MAKEFILE

/*
    This preprocessor directive causes the dlib headers to pull in all the code
    that would normally be built in dlib/all/source.cpp. Thus if you #define
    NO_MAKEFILE you won't have to add dlib/all/source.cpp to your project. The
    only time this is useful is when your project consists of a single
    translation unit (i.e. a single cpp file). In this instance NO_MAKEFILE
    allows you to easily build your project on the command line by saying
    something like g++ -DNO_MAKEFILE project.cpp. But again, this is only for
    single cpp file projects. If you use NO_MAKEFILE with projects that contain
    more than one cpp file you will get linker errors about multiply defined
    symbols.

    Also note that if you use this macro then the stack trace functionality in
    the library will be disabled.
*/

// #define DLIB_THREAD_POOL_TIMEOUT <time-in-milliseconds>

/*
    If you use dlib to create your threads then you receive the benefit of the
    dlib dynamic thread pool (Note that the dlib::thread_pool object is
    something else unrelated to this so don't confuse the two). This pool
    enables dlib to spawn new threads very rapidly since it draws threads back
    out of its thread pool when the pool isn't empty.

    Thus, when a thread that was created by dlib ends it actually goes back into
    the dlib thread pool and waits DLIB_THREAD_POOL_TIMEOUT milliseconds before
    totally terminating and releasing its resources back to the operating
    system. The default timeout used by this library is 30,000 milliseconds
    (30 seconds). You may however change this to whatever you like by defining
    DLIB_THREAD_POOL_TIMEOUT to some new value.
*/




#endif
