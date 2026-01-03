.PHONY: clean build run-all run-proxy run-desktop

clean:
	rm -rf desktop/build/*

build:
	echo "Updating python packages..."
	pip install -r requirements.txt
	echo "Updating flutter packages and building linux desktop app.."
	cd desktop && flutter pub upgrade && flutter build linux

run-all:
	$(MAKE) -j 2 run-proxy run-desktop

run-proxy:
	python3 -m api.app

run-desktop:
	chmod +x desktop/build/linux/x64/release/bundle/desktop
	./desktop/build/linux/x64/release/bundle/desktop
