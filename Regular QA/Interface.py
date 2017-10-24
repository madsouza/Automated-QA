import pyglet
from pyglet.gl import gl
import Tests


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

window = pyglet.window.Window()
label = pyglet.text.Label('QA submission', font_name='Times New Roman', font_size=34,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center', height=window.height)


machineLabels = []
for i in range(1, 7):
    machineLabels.append(pyglet.text.Label('RT%s' % i,
                         font_name='Times New Roman',
                         font_size=12,
                         x=i*window.width/7, y=7*window.height/8,
                         anchor_x='center', anchor_y='center'))


gl.glClearColor(*background_color)
@window.event
def on_draw():
    window.clear()
    label.draw()
    [l.draw() for l in machineLabels]
    # label1.draw()
    # label2.draw()
    # label3.draw()
    # label4.draw()
    # label5.draw()
    # label6.draw()


@window.event
def on_key_press(symbol, modifiers):
    print 'A key was pressed'

pyglet.app.run()