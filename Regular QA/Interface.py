import pyglet
from pyglet.gl import gl
import Tests

RT1 = []
RT2 = []
RT3 = []
RT4 = []
RT5 = []
RT6 = []

tests = Tests.tests()
unique_tests = list(set([t.split('_')[0] for t in tests.test_info.keys()]))
unique_tests.sort()
organized_tests = {}

for item in tests.test_info:
    parent_test = item.split('_')[0]
    if parent_test not in organized_tests:
        organized_tests[parent_test] = [item]
    else:
        organized_tests[parent_test].append(item)

print organized_tests
background_color = (0, .5, .8, 1)


window = pyglet.window.Window(1000, 600)

label = pyglet.text.Label('QA submission', font_name='Times New Roman', font_size=30,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center', height=window.height)


machineLabels = []

for i in range(1, 7):
    machineLabels.append(pyglet.text.Label('RT%s' % i,
                         font_name='Times New Roman',
                         font_size=14,
                         x=i*window.width/7, y=7*window.height/8,
                         anchor_x='center', anchor_y='center'))

remaining_space = [6.5*window.height/8, 0]

spacing = (remaining_space[0] - remaining_space[1])/len(unique_tests)

unique_test_labels = []
unique_test_sprites = []
child_test_labels = []
count = 0

for item in unique_tests:
    unique_test_labels.append(pyglet.text.Label(item,
                              font_name='Times New Roman',
                              font_size=12,
                              x=window.width/7, y=remaining_space[0] - count*spacing,
                              anchor_x='center', anchor_y='center'))

    if len(organized_tests[item]) > 1:
        x_spacing = (window.width - 2*window.width/7)/len(organized_tests[item])
        print(x_spacing)
        x_count = 0

        for child in sorted(organized_tests[item]):
            child_test_labels.append(pyglet.text.Label(child,
                                                       font_name='Times New Roman',
                                                       font_size=8,
                                                       x=2*window.width/7 + x_count*x_spacing,
                                                       y=remaining_space[0] - count * spacing,
                                                       anchor_x='center', anchor_y='center'))
            x_count += 1
    green = pyglet.image.load('green.png')
    green.width = int(window.width/7)
    green.height = int(spacing)
    unique_test_sprites.append(pyglet.sprite.Sprite(green, x=window.width/7, y=remaining_space[0] - count*spacing))
    count += 1

gl.glClearColor(*background_color)


@window.event
def on_draw():
    window.clear()
    label.draw()
    [l.draw() for l in machineLabels]
    [l.draw() for l in unique_test_labels]
    [l.draw() for l in child_test_labels]
    [l.draw() for l in unique_test_sprites]

pyglet.app.run()
