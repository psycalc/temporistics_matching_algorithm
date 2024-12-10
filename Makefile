SHELL = /bin/bash

test:
	(docker-compose up --build --abort-on-container-exit --exit-code-from test test; \
	 docker-compose down -v) 2>&1 | tee >(xclip -sel clip)