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

for t in tests.test_info:
    parent_test = t.split('_')[0]
    if parent_test not in organized_tests:
        organized_tests[parent_test] = [t]
    else:
        organized_tests[parent_test].append(t)

print organized_tests
background_color = (0.98, 0.98, 0.98, 1)


# window = pyglet.window.Window(1000, 600)


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.label = None
        print Window.width.__get__(self)
        print getattr(Window, 'width')
        self.machineLabels = []
        self.machine_sprites = []
        self.unique_test_labels = []
        self.unique_test_sprites = []
        self.child_test_labels = []
        self.background_color = (0.98, 0.98, 0.98, 1)
        self.generate_labels_sprites()

    def generate_labels_sprites(self):

        self.label = pyglet.text.Label('QA submission', font_name='Helvetica', font_size=30,
                                       x=Window.width.__get__(self) // 2, y=Window.height.__get__(self) // 2,
                                       anchor_x='center', anchor_y='center', height=Window.height.__get__(self),
                                       color=(0, 147, 199, 255))

        for i in range(1, 7):
            self.machineLabels.append(pyglet.text.Label('RT%s' % i,
                                                        font_name='Helvetica',
                                                        font_size=14,
                                                        x=i * Window.width.__get__(self) / 7,
                                                        y=7 * Window.height.__get__(self) / 8,
                                                        anchor_x='center', anchor_y='center', color=(0, 147, 199, 255)))
            green = pyglet.image.load('green.png')
            green.width = int(i*Window.width.__get__(self) / 7)
            green.height = int(7 * Window.height.__get__(self) / 8)
            temp_sprite = pyglet.sprite.Sprite(green, x=i*Window.width.__get__(self) / 7 / 2,
                                               y=7 * Window.height.__get__(self) / 8)
            #temp_sprite.visible = False
            self.machine_sprites.append([temp_sprite, temp_sprite.position, [temp_sprite.x + temp_sprite.width,
                                                                             temp_sprite.y + temp_sprite.height]])
            # self.machine_sprites.append()

        remaining_space = [6.5 * Window.height.__get__(self) / 8, 0]

        spacing = (remaining_space[0] - remaining_space[1]) / len(unique_tests)

        count = 0

        for item in unique_tests:
            self.unique_test_labels.append(pyglet.text.Label(item, font_name='Helvetica', font_size=12,
                                                             x=Window.width.__get__(self) / 7,
                                                             y=remaining_space[0] - count * spacing,
                                                             anchor_x='center', anchor_y='center',
                                                             color=(0, 147, 199, 255)))

            if len(organized_tests[item]) > 1:
                x_spacing = (Window.width.__get__(self) - 2 * Window.width.__get__(self) / 7) / \
                            len(organized_tests[item])

                x_count = 0

                for child in sorted(organized_tests[item]):
                    self.child_test_labels.append(pyglet.text.Label(child, font_name='Helvetica', font_size=8,
                                                                    x=2 * Window.width.__get__(self) / 7 +
                                                                    x_count * x_spacing,
                                                                    y=remaining_space[0] - count * spacing,
                                                                    anchor_x='center', anchor_y='center',
                                                                    color=(0, 147, 199, 255)))
                    x_count += 1
            green = pyglet.image.load('green.png')
            green.width = int(Window.width.__get__(self) / 7)
            green.height = int(spacing - 2)
            print remaining_space[0]
            temp_sprite = pyglet.sprite.Sprite(green, x=Window.width.__get__(self) / 7 / 2,
                                               y=remaining_space[0] - count * spacing -
                                               0.5 * spacing)
            temp_sprite.visible = False
            self.unique_test_sprites.append([temp_sprite, temp_sprite.position, [temp_sprite.x + temp_sprite.width,
                                                                                 temp_sprite.y + temp_sprite.height]])
            count += 1

    def on_draw(self):
        gl.glClearColor(*background_color)
        Window.clear(self)
        self.label.draw()
        [l[0].draw() for l in self.unique_test_sprites]
        [l[0].draw() for l in self.machine_sprites]
        [l.draw() for l in self.machineLabels]
        [l.draw() for l in self.unique_test_labels]
        [l.draw() for l in self.child_test_labels]

    def on_mouse_press(self, x, y, button, modifiers):

        # print self.unique_test_sprites[0][1][0]
        # print x
        # print self.unique_test_sprites[0][2][0]
        # print self.unique_test_sprites[0][1][0] < x < self.unique_test_sprites[0][2][0] and
        # self.unique_test_sprites[0][1][1] < y < self.unique_test_sprites[0][2][1]
        for n in range(0, len(self.unique_test_sprites)):
            item = self.unique_test_sprites[n]
            if item[1][0] < x < item[2][0] and item[1][1] < y < item[2][1]:
                print True
                self.unique_test_sprites[n][0].visible = not self.unique_test_sprites[n][0].visible
                print self.unique_test_sprites[n][0].visible
                break


def main():
    window = Window(width=1000, height=600, caption='QA Submitter 9000', resizable=True)
    pyglet.app.run()


main()
