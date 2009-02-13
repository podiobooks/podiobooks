#!/bin/bash

# makegraph.sh
# Author: Jason Penney (http://jasonpenney.net/)

# START CONFIG

# set "models" to space separated list of models to generate graphs for
# models="model1 model2"
models="main"

# set "formats" to list of diagram formats
# formats="pdf svg png dia"
formats="pdf"

# END CONFIG

# verify we can run
type dot 2>&1 >/dev/null

if [[ "$?" != "0" ]]; then
    cat <<EOF 1>&2
Unable to find 'dot' command in your path.
Please ensure you have graphviz installed
EOF
    exit 2
fi

startdir=$(dirname $0)
# ensure we have an absoute path
echo $startdir | grep -q ^/
if [[ "$?" != "0" ]]; then
    startdir="$(pwd)/${startdir}"
fi

(
    cd "${startdir}/../../pbsite"
    if [[ -f "modelviz.py" ]]; then
        echo "modelviz.py already present in $(pwd).  Aborting" 2>&1
        exit 3;
    fi
    cp -f "${startdir}/../contrib/modelviz.py" .
    python ./modelviz.py ${models} > ${startdir}/schema.dot
    rm -f modelviz.py
)


if [[ ! -f "${startdir}/schema.dot" ]]; then
    echo "Unable to generate 'schema.dot'" 1>&2
    exit 1;
fi

for format in ${formats}; do
    echo "generating schema.${format}"
    dot ${startdir}/schema.dot -T${format} -o ${startdir}/schema.${format}
done

