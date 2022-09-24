#!/usr/bin/env bash
date
cd $(dirname $0)
pwd
cat ../../../mathz/shared/fuzzlib\
 ../../../mathz/articles/sets/sets.sty\
 ../../../mathz/articles/sets/sets.tex\
 ../../../mathz/articles/topological-spaces/topological-spaces.sty\
 ../../../mathz/articles/topological-spaces/topological-spaces.tex\
 ../../../mathz/articles/groups/groups.sty\
 ../../../mathz/articles/groups/groups.tex\
 ../../../mathz/articles/real-numbers/real-numbers.sty\
 ../../../mathz/articles/real-numbers/real-numbers.tex\
 so3-so5.sty > so3-so5.prelude
fuzz -d -p so3-so5.prelude so3-so5
