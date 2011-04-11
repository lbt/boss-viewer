default:
	echo "Nothing to do"

install:
	install -d $(DESTDIR)/var/lib/boss-viewer/boss-viewer/log/
	install -m 644 boss-viewer.ru $(DESTDIR)/var/lib/boss-viewer/
	install -m 755 log.run $(DESTDIR)/var/lib/boss-viewer/boss-viewer/log/run
	install -m 755 daemon.run $(DESTDIR)/var/lib/boss-viewer/boss-viewer/run
