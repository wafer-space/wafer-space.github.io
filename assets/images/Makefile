
# logo-raw.webp -- 2880x768

# logo.webp     --  240x64  == /12
# logo@2x.webp  --  120x32  == /22.5

logo@2x.webp: logo-raw.webp
	convert $< -resize 240x64 $@

logo.webp: logo-raw.webp
	convert $< -resize 120x32 $@

logo-light@2x.webp: logo-light-raw.webp
	convert $< -resize 240x64 $@

logo-light.webp: logo-light-raw.webp
	convert $< -resize 120x32 $@

update:
	rm logo@2x.webp
	rm logo.webp
	make all

all: logo.webp logo@2x.webp logo-light.webp logo-light@2x.webp
	@true
