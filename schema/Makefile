.PHONY: FORCE
.SUFFIXES:
.DELETE_ON_ERROR:

YAMLS:=ga4gh.yaml vrs.yaml
JSONS:=${YAMLS:.yaml=.json}

all: ${JSONS}

%.json: %.yaml
	./y2j <$< >$@

## # npm install -g json-dereference-cli
## %.json: %.yaml
## 	json-dereference -s $< -o $@


watch:
	-while true; do ls -1 *.yaml | entr -dn make ${JSONS}; done
