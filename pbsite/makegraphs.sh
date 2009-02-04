#!/bin/bash
cd `dirname $0`
python modelviz.py main >schema.dot && dot schema.dot  -Tpdf -o schema.pdf
