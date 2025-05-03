
# logo-raw.webp -- 2010x720

logo@2x.webp: logo-raw.webp
	convert $< -resize 240x64 $@


logo.webp: logo-raw.webp
	convert $< -resize 120x32 $@

update:
	rm logo@2x.webp
	rm logo.webp
	make all

all: logo.webp logo@2x.webp
	@true
