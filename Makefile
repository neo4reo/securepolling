DOC_FORMAT = html
.PHONY: doc sync

doc:
	cd doc && gmake ${DOC_FORMAT}
	find doc/_build/${DOC_FORMAT} -type f -exec fossil uv add '{}' \;
sync:
	fossil uv sync
	fossil configuration sync all
	fossil push
