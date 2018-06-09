# Bayesian Network Weighted Model Counting tools

This package contains:

* Bayesian Networks (BN) in HUGIN format
* BN variable elimination orderings
* BN to Conjunctive Normal Form Compiler
* BN to WPBDD compiler
* BN to OBDD compiler (using CUDD)
* BN to ZBDD compiler (using CUDD)
* BN to SDD compiler (using SDD)
* BN to d-DNNF compiler (using ACE)
* Model Counter for inference
* A testing suite

## Installation

Binaries can be found in directory `bin`, so building is not necessary.

Regardless, in order to retreive (and update) all neccesary repositories, type:
> git submodule update --init --recursive

To build, type:
> make

## Testing

To test the compilers use test script `run.py` in directory `test`, for example:
> ./test/run.py --test compilation --network asia --bdd tdmg ace


