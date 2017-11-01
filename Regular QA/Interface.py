import pyglet
from pyglet.gl import gl
import Tests


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
        self.active_machine = 0
        self.tests_to_submit = [[], [], [], [], [], []]
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
            green.width = int(Window.width.__get__(self) / 7)
            green.height = int(Window.height.__get__(self) / 8 - 40)

            temp_sprite = pyglet.sprite.Sprite(green, x=i*Window.width.__get__(self) / 7 -
                                                        Window.width.__get__(self) / 7/2,
                                               y=(6.75 * Window.height.__get__(self) / 8))
            # temp_sprite.visible = False
            if i > 1:
                temp_sprite.visible = False

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
                                                                                 temp_sprite.y + temp_sprite.height],
                                             item])

            [a.append(False) for a in self.tests_to_submit]
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

        cycle = True
        while cycle:
            for n in range(0, len(self.machine_sprites)):
                item = self.machine_sprites[n]
                if item[1][0] < x < item[2][0] and item[1][1] < y < item[2][1]:
                    if self.machine_sprites[n][0].visible:
                        print 'is visible'
                        cycle = False
                    else:
                        print 'turned on'
                        self.machine_sprites[n][0].visible = not self.machine_sprites[n][0].visible
                        self.active_machine = n
                        print self.active_machine
                        for a in range(0, len(self.machine_sprites)):
                            if a != n:
                                self.machine_sprites[a][0].visible = False

                        for a in range(0, len(self.unique_test_sprites)):
                            self.unique_test_sprites[a][0].visible = self.tests_to_submit[self.active_machine][a]

                        cycle = False

            for n in range(0, len(self.unique_test_sprites)):
                item = self.unique_test_sprites[n]
                if item[1][0] < x < item[2][0] and item[1][1] < y < item[2][1]:
                    self.unique_test_sprites[n][0].visible = not self.unique_test_sprites[n][0].visible
                    self.tests_to_submit[self.active_machine][n] = self.unique_test_sprites[n][0].visible
                    print self.unique_test_sprites[n][0].visible
                    break

            cycle = False


def main():
    window = Window(width=1000, height=600, caption='QA Submitter v0.5', resizable=True)
    pyglet.app.run()


main()
