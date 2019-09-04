# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Sep 04, 2019 at 04:48 PM -0400

BINPATH	:=	gen
SRCPATH	:=	gen

# Compiler settings
COMPILER	:=	$(shell root-config --cxx)
CXXFLAGS	:=	$(shell root-config --cflags)
LINKFLAGS	:=	$(shell root-config --libs)
ADDFLAGS	:=	-Iinclude


$(BINPATH)/%.exe: $(SRCPATH)/%.cpp
	$(COMPILER) $(CXXFLAGS) $(ADDFLAGS) -o $@ $(SRCPATH)/$(basename $(@F)).cpp $(LINKFLAGS)
