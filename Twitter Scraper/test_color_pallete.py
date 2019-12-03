import colorgram  #pip install colorgram.py

# Extract 6 colors from an image.
colors = colorgram.extract('test.jpg', 6)

# colorgram.extract returns Color objects, which let you access
# RGB, HSL, and what proportion of the image was that color.
first_color = colors[0]
rgb = first_color.rgb # e.g. (255, 151, 210)
hsl = first_color.hsl # e.g. (230, 255, 203)
proportion  = first_color.proportion # e.g. 0.34

# RGB and HSL are named tuples, so values can be accessed as properties.
# These all work just as well:
red = rgb[0]
red = rgb.r
saturation = hsl[1]
saturation = hsl.s


for color in colors:
	print color

rows = int(len(colors)/100) if len(colors) > 100 else 8
pallete = sorted(colors, key=lambda rgb : step(rgb,rows))

# rows = int(len(pallete)/100) if len(pallete) > 100 else 8
pallete = pallete[:len(pallete)-len(pallete)%rows]

palette = np.array(chunkIt(pallete, rows))
# indices = np.random.randint(0, len(palette), size=(4, 6))
# print(palette)
plt.imshow(palette)

ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
plt.title("Color Pallete for "+ screen_name, fontsize=18)
ymin, ymax = ax.get_ylim()
print(ymax)
plt.text(0, -1 * ymax/10, "Data source: www.twitter.com", fontsize=10)
plt.axis('off')
plt.tight_layout()
# plt.colorbar()
photoName = screen_name + "_pallete" + '.pdf'
plt.savefig(path + photoName)

plt.imshow()
