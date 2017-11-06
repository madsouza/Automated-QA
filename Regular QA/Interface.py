import pyglet
from pyglet.gl import gl
import Tests


# get all our test names and get unique parent tests (i.e ML11 from ML11_e and ML11_p)
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


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.label = None
        self.width = Window.width.__get__(self)
        self.height = Window.height.__get__(self)
        print getattr(Window, 'width')
        self.machineLabels = []
        self.machine_sprites = []
        self.unique_test_labels = []
        self.unique_test_sprites = []
        self.child_test_labels = []
        self.button_sprites = []
        self.background_color = (0.98, 0.98, 0.98, 1)
        self.active_machine = 0
        #                      RT1 RT2 RT3 RT4 RT5 RT6
        self.tests_to_submit = [[], [], [], [], [], []]
        self.vertex_list = None
        self.generate_labels_sprites()
        self.generate_button()

    def generate_labels_sprites(self):

        self.label = pyglet.text.Label('QA submission', font_name='Helvetica', font_size=30,
                                       x=self.width // 2, y=self.height // 2,
                                       anchor_x='center', anchor_y='center', height=self.height,
                                       color=(0, 147, 199, 255))

        # display machine name and sprites at the top of the interface
        for i in range(1, 7):
            self.machineLabels.append(pyglet.text.Label('RT%s' % i,
                                                        font_name='Helvetica',
                                                        font_size=14,
                                                        x=i * self.width / 7,
                                                        y=7 * self.height / 8,
                                                        anchor_x='center', anchor_y='center', color=(0, 147, 199, 255)))

            green = pyglet.image.load('green.png')
            green.width = int(self.width / 7)
            green.height = int(self.height / 8 - 40)

            temp_sprite = pyglet.sprite.Sprite(green, x=i*self.width / 7 -
                                                        self.width / 7/2,
                                               y=(6.75 * self.height / 8))

            # set the first machine label to be selected (default machine) by setting the visibility of the others to
            #   False
            if i > 1:
                temp_sprite.visible = False

            # store in list of the form [sprite, [x,y coordinates of bottom left], [x,y coordinates of top right]]
            self.machine_sprites.append([temp_sprite, temp_sprite.position, [temp_sprite.x + temp_sprite.width,
                                                                             temp_sprite.y + temp_sprite.height]])

        # lets see how much space is left in the window
        remaining_space = [6.5 * self.height / 8, 0]

        # divide that by the total number of tests
        spacing = (remaining_space[0] - remaining_space[1]) / len(unique_tests)

        count = 0

        # set parent tests along the left column, if child tests are present display them next to the parents
        for item in unique_tests:
            self.unique_test_labels.append(pyglet.text.Label(item, font_name='Helvetica', font_size=12,
                                                             x=self.width / 7,
                                                             y=remaining_space[0] - count * spacing,
                                                             anchor_x='center', anchor_y='center',
                                                             color=(0, 147, 199, 255)))

            if len(organized_tests[item]) > 1:
                x_spacing = (self.width - 2 * self.width / 7) / \
                            len(organized_tests[item])

                x_count = 0

                for child in sorted(organized_tests[item]):
                    self.child_test_labels.append(pyglet.text.Label(child, font_name='Helvetica', font_size=8,
                                                                    x=2 * self.width / 7 +
                                                                    x_count * x_spacing,
                                                                    y=remaining_space[0] - count * spacing,
                                                                    anchor_x='center', anchor_y='center',
                                                                    color=(0, 147, 199, 255)))
                    x_count += 1

            green = pyglet.image.load('green.png')
            green.width = int(self.width / 7)
            green.height = int(spacing - 2)
            print remaining_space[0]
            temp_sprite = pyglet.sprite.Sprite(green, x=self.width / 7 / 2,
                                               y=remaining_space[0] - count * spacing -
                                               0.5 * spacing)
            temp_sprite.visible = False
            self.unique_test_sprites.append([temp_sprite, temp_sprite.position, [temp_sprite.x + temp_sprite.width,
                                                                                 temp_sprite.y + temp_sprite.height],
                                             item])

            [a.append(False) for a in self.tests_to_submit]
            count += 1

    def generate_button(self):
        self.vertex_list = pyglet.graphics.vertex_list(8, ('v2f', (  # horizontal lines
                                                                   5.5 * self.width / 7,
                                                                   6.9 * self.height / 7,
                                                                   6.5 * self.width / 7,
                                                                   6.9 * self.height / 7,

                                                                   5.5 * self.width / 7,
                                                                   6.5 * self.height / 7,
                                                                   6.5 * self.width / 7,
                                                                   6.5 * self.height / 7,

                                                                   # vertical lines
                                                                   5.5 * self.width / 7,
                                                                   6.9 * self.height / 7,
                                                                   5.5 * self.width / 7,
                                                                   6.5 * self.height / 7,

                                                                   6.5 * self.width / 7,
                                                                   6.9 * self.height / 7,
                                                                   6.5 * self.width / 7,
                                                                   6.5 * self.height / 7,)),
                                                       ('c3B', (0, 0, 200)*8))
        green = pyglet.image.load('green.png')
        green.width = int(1.01 * self.width / 7)
        green.height = int(0.4 * self.height / 7)
        temp_sprite = pyglet.sprite.Sprite(green, x=5.5 * self.width / 7,
                                           y=6.5 * self.height / 7)
        item = 'button'
        temp_sprite.visible = True
        self.button_sprites.append([temp_sprite, temp_sprite.position, [temp_sprite.x + temp_sprite.width,
                                                                        temp_sprite.y + temp_sprite.height],
                                         item])

        green = pyglet.image.load('green_2.jpg')
        green.width = int(1.01 * self.width / 7)
        green.height = int(0.4 * self.height / 7)
        temp_sprite = pyglet.sprite.Sprite(green, x=5.5 * self.width / 7,
                                           y=6.5 * self.height / 7)
        item = 'button'
        temp_sprite.visible = False
        self.button_sprites.append([temp_sprite, temp_sprite.position, [temp_sprite.x + temp_sprite.width,
                                                                        temp_sprite.y + temp_sprite.height],
                                         item])

        self.unique_test_labels.append(pyglet.text.Label('SUBMIT', font_name='Helvetica', font_size=14,
                                                         x=6 * self.width / 7,
                                                         y=6.7 * self.height / 7,
                                                         anchor_x='center', anchor_y='center',
                                                         color=(0, 147, 199, 255), bold=True))

    def on_draw(self):
        gl.glClearColor(*background_color)
        Window.clear(self)
        self.label.draw()
        [l[0].draw() for l in self.unique_test_sprites]
        [l[0].draw() for l in self.machine_sprites]
        [l[0].draw() for l in self.button_sprites]
        [l.draw() for l in self.machineLabels]
        [l.draw() for l in self.unique_test_labels]
        [l.draw() for l in self.child_test_labels]
        self.vertex_list.draw(pyglet.gl.GL_LINES)

    def on_mouse_motion(self, x, y, dx, dy):
        if 5.5 * self.width / 7 < x < 6.5 * self.width / 7 and \
           6.5 * self.height / 7 < y < 6.9 * self.height / 7:
            self.button_sprites[0][0].visible = False
            self.button_sprites[1][0].visible = True
        else:
            self.button_sprites[0][0].visible = True
            self.button_sprites[1][0].visible = False

    def on_mouse_press(self, x, y, button, modifiers):

        cycle = True
        while cycle:
            if 5.5 * self.width / 7 < x < 6.5 * self.width / 7 and \
               6.5 * self.height / 7 < y < 6.9 * self.height / 7:
                print ('submit')
                cycle = False
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
    window = Window(width=1000, height=600, caption='QA Submitter v0.7')
    pyglet.app.run()


main()
