#!/usr/bin/env bash
date
cd $(dirname $0)
pwd
cat ../../../mathz/shared/fuzzlib\
 so3-so5.sty > so3-so5.prelude
fuzz -d -p so3-so5.prelude so3-so5
