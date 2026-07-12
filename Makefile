.PHONY: clean update-deps run-all run-all-desktop run-proxy run-desktop run-web

clean:
	rm -rf desktop/build/*

update-deps:
	echo "Updating python packages..."
	pip install -r requirements.txt
	echo "Updating flutter packages and building web app.."
	cd desktop && flutter pub upgrade && flutter build web --release

# Opcja 1: Odpala Backend + Web przez Nginx (Dla wielu osób przez przeglądarkę)
run-all:
	mkdir -p desktop/data/csv
	chmod u+rwx desktop/data/csv
	$(MAKE) -j 2 run-proxy run-web

# Opcja 2: Odpala Backend + Lokalną wersję okienkową Linux na RPi
run-all-desktop:
	mkdir -p desktop/data/csv
	chmod u+rwx desktop/data/csv
	$(MAKE) -j 2 run-proxy run-desktop

run-proxy:
	python3 -m api.app

# Serwowanie aplikacji przez Nginx
run-web:
	echo "Deploying Flutter Web to Nginx..."
	rm -rf /var/www/html/*
	cp -r desktop/build/web/* /var/www/html/
	echo "Ensuring Nginx service is running..."
	sudo systemctl start nginx
	echo "Application is live at http://localhost (or your RPi IP)"

# Uruchomienie natywnej aplikacji Linux (Desktop)
run-desktop:
	chmod +x desktop/build/linux/x64/release/bundle/desktop
	./desktop/build/linux/x64/release/bundle/desktop
