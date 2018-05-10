import pyglet
from pyglet.gl import gl
import Tests
import os
import qatrack
import copy


# copies files from qa folder and puts it in our directory
os.system("del_copy.bat")

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


class Rectangle(object):
    '''Draws a rectangle into a batch.'''

    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
                                     ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
                                     ('c4B', [200, 200, 220, 255] * 4)
                                     )


class TextWidget(object):
    def __init__(self, text, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
                                dict(color=(0, 0, 0, 255))
                                )
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline
        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad,
                                   x + width + pad, y + height + pad, batch)

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)


class AuthenticationWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(AuthenticationWindow, self).__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.width = AuthenticationWindow.width.__get__(self)
        self.height = AuthenticationWindow.height.__get__(self)
        self.labels = pyglet.graphics.Batch()
        self.spr = pyglet.graphics.Batch()
        self.background_color = (0.98, 0.98, 0.98, 1)
        self.instruction_label = pyglet.text.Label('Please log in using QA track login', font_name='Helvetica',
                                                   font_size=12, x=100, y=175, color=(0, 147, 199, 255),
                                                   bold=True, batch=self.labels)
        self.user_text = pyglet.text.Label('Username', font_name='Helvetica', font_size=12, x=100, y=135,
                                           color=(0, 147, 199, 255), bold=True, batch=self.labels)
        self.pass_text = pyglet.text.Label('Password', font_size=12, x=100, y=85,
                                           color=(0, 147, 199, 255), bold=True, batch=self.labels)

        self.vertex_list = pyglet.graphics.vertex_list(16, ('v2f', (
            # User name
            # horizontal lines
            200,
            128,
            400,
            128,

            200,
            150,
            400,
            150,

            # vertical lines
            200,
            128,
            200,
            150,

            400,
            128,
            400,
            150,

            # password
            # Horizontal lines
            200,
            100,
            400,
            100,

            200,
            78,
            400,
            78,

            # Vertical lines
            200,
            100,
            200,
            78,

            400,
            100,
            400,
            78,
            )),
                                                       ('c3B', (0, 0, 200) * 16))

        white = pyglet.image.load('grey.png')
        white.width = int(200)
        white.height = int(22)
        green = pyglet.image.load('green.png')
        green.width = int(200)
        green.height = int(30)

        green2 = pyglet.image.load('green_2.jpg')
        green2.width = int(200)
        green2.height = int(30)
        # self.user_sprite = pyglet.sprite.Sprite(white, x=200, y=128, batch=self.spr)
        # self.user_sprite.visible = False
        self.user_input = pyglet.text.Label('', font_name='Helvetica', font_size=12, x=205, y=135,
                                            color=(0, 147, 199, 255),bold=True)

        # self.pass_sprite = pyglet.sprite.Sprite(white, x=200, y=78, batch=self.spr)
        # self.pass_sprite.visible = True

        self.widgets = [
            TextWidget('user', 205, 130, self.width - 210, self.batch),
            TextWidget('', 205, 80, self.width - 210, self.batch)
        ]
        self.text_cursor = self.get_system_mouse_cursor('text')

        self.focus = None
        self.set_focus(self.widgets[0])

        self.confirm_button = pyglet.sprite.Sprite(green, x=150, y=20, batch=self.spr)
        self.confirm_text = pyglet.text.Label('Log In', font_name='Helvetica', font_size=12, x=225, y=28,
                                              color=(0, 147, 199, 255), bold=True, batch=self.labels)

    def on_draw(self):
        gl.glClearColor(*background_color)
        AuthenticationWindow.clear(self)
        self.spr.draw()
        self.user_input.draw()
        self.vertex_list.draw(pyglet.gl.GL_LINES)
        self.batch.draw()
        self.labels.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_mouse_cursor(self.text_cursor)
                break
        else:
            self.set_mouse_cursor(None)

    def on_mouse_press(self, x, y, button, modifiers):
        # if 200 < x < 400 and 128 < y < 150:
        #     self.user_sprite.visible = True
        #     self.pass_sprite.visible = False
        # elif 200 < x < 400 and 78 < y < 100:
        #     self.user_sprite.visible = False
        #     self.pass_sprite.visible = True
        # else:
        #     self.user_sprite.visible = False
        #     self.pass_sprite.visible = False

        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_focus(widget)
                break
        else:
            self.set_focus(None)

        if self.focus:
            self.focus.caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus:
            self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_text(self, text):
        if self.focus:
            self.focus.caret.on_text(text)

    def on_text_motion(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.TAB:
            if modifiers & pyglet.window.key.MOD_SHIFT:
                dir = -1
            else:
                dir = 1

            if self.focus in self.widgets:
                i = self.widgets.index(self.focus)
            else:
                i = 0
                dir = 0

            self.set_focus(self.widgets[(i + dir) % len(self.widgets)])

        elif symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)


class ProgressWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(ProgressWindow, self).__init__(*args, **kwargs)
        self.width = ProgressWindow.width.__get__(self)
        self.height = ProgressWindow.height.__get__(self)
        self.label = pyglet.text.Label('Please wait, submission in progress', font_name='Helvetica', font_size=20,
                                        x=250,
                                        y=50,
                                        anchor_x='center', anchor_y='center',
                                        color=(0, 147, 199, 255), bold=True)
        self.background_color = (0.98, 0.98, 0.98, 1)

    def on_draw(self):
        gl.glClearColor(*background_color)
        ProgressWindow.clear(self)
        self.label.draw()


class ConfirmationWindow(pyglet.window.Window):

    def __init__(self, selected_tests, *args, **kwargs):
        super(ConfirmationWindow, self).__init__(*args, **kwargs)
        self.width = ConfirmationWindow.width.__get__(self)
        self.height = ConfirmationWindow.height.__get__(self)
        self.selected_tests = selected_tests
        self.background_color = (0.98, 0.98, 0.98, 1)
        self.labels = []
        self.is_not_clicked = 0
        self.vertex_list = pyglet.graphics.vertex_list(8, ('v2f', (
            # horizontal lines
            2 * self.width / 7,
            1 * self.height / 7,
            5 * self.width / 7,
            1 * self.height / 7,

            2 * self.width / 7,
            0.25 * self.height / 7,
            5 * self.width / 7,
            0.25 * self.height / 7,

            # vertical lines
            2 * self.width / 7,
            1 * self.height / 7,
            2 * self.width / 7,
            0.25 * self.height / 7,

            5 * self.width / 7,
            1 * self.height / 7,
            5 * self.width / 7,
            0.25 * self.height / 7,)), ('c3B', (0, 0, 200) * 8))

        for i in range(1, 7):
            self.labels.append(pyglet.text.Label('RT%s' % i, font_name='Helvetica', font_size=18,
                                                 x=i * self.width / 7, y=7.5 * self.height / 8, bold=True,
                                                 anchor_x='center', anchor_y='center',
                                                 color=(0, 147, 199, 255)))
            remaining_height = [int(6.5 * self.height / 8), int(1.5 * self.height / 8)]
            if len(self.selected_tests['RT%s' % i]) > 0:
                spacing = int((remaining_height[0] - remaining_height[1])/(len(self.selected_tests['RT%s' % i])))
            for x in range(0, len(self.selected_tests['RT%s' % i])):
                self.labels.append(pyglet.text.Label(self.selected_tests['RT%s' % i][x], font_name='Helvetica',
                                                     font_size=12, bold=True,
                                                     x=i * self.width / 7, y=remaining_height[0] - x * spacing,
                                                     anchor_x='center', anchor_y='center',
                                                     color=(0, 147, 199, 255)))

        green = pyglet.image.load('green.png')
        green.width = int(3 * self.width / 7)
        green.height = int(0.75 * self.height / 7)

        self.idle_button = pyglet.sprite.Sprite(green, x=2 * self.width / 7, y=0.25 * self.height / 7)

        green_2 = pyglet.image.load('green_2.jpg')
        green_2.width = int(3 * self.width / 7)
        green_2.height = int(0.75 * self.height / 7)

        self.mouse_over_button = pyglet.sprite.Sprite(green_2, x=2 * self.width / 7, y=0.25 * self.height / 7)
        self.mouse_over_button.visible = False

        self.confirm_label = pyglet.text.Label('CONFIRM', font_name='Helvetica', font_size=18,
                                                         x=3.5 * self.width / 7,
                                                         y=0.625 * self.height / 7,
                                                         anchor_x='center', anchor_y='center',
                                                         color=(0, 147, 199, 255), bold=True)


    def on_draw(self):
        gl.glClearColor(*background_color)
        ConfirmationWindow.clear(self)
        [l.draw() for l in self.labels]
        self.mouse_over_button.draw()
        self.idle_button.draw()
        self.vertex_list.draw(pyglet.gl.GL_LINES)
        self.confirm_label.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        if 2 * self.width / 7 < x < 5 * self.width / 7 and \
                                                0.25 * self.height / 7 < y < self.height / 7:
            self.idle_button.visible = False
            self.mouse_over_button.visible = True
        else:
            self.idle_button.visible = True
            self.mouse_over_button.visible = False

    def on_mouse_press(self, x, y, button, modifiers):

        if 2 * self.width / 7 < x < 5 * self.width / 7 and \
                                                0.25 * self.height / 7 < y < self.height / 7 \
                and self.is_not_clicked == 0:
            self.is_not_clicked = 1
            progress_window = ProgressWindow(width=500, height=100)
            self.confirm_label.text = 'PLEASE WAIT'
            obtained_values = []
            for mach, list_val in sorted(self.selected_tests.items()):
                for val in list_val:
                    # obtained_values.append([mach, val, tests.get_test(mach, val)])
                    obtained_values += tests.get_test(mach, val)
            print obtained_values
            print self.selected_tests
            text_labels = [str(x.text) for x in self.labels]
            print obtained_values
            for item in obtained_values:
                if type(item[2]) != list:
                    if '_' in item[1]:
                        parent_test_name = item[1][:4]
                    else:
                        parent_test_name = item[1]
                    mach_index = text_labels.index(item[0])
                    indices = [i for i, x in enumerate(text_labels) if x == parent_test_name]

                    final_index = (e for e in indices if e > mach_index).next()
                    self.labels[final_index].text = '%s: %s' % (item[1], item[2])
                else:
                    qatrack.submit(qatrack.test_number(item[0], item[1]), item[2])
                    if '_' in item[1]:
                        parent_test_name = item[1][:4]
                    else:
                        parent_test_name = item[1]
                    mach_index = text_labels.index(item[0])
                    indices = [i for i, x in enumerate(text_labels) if x == parent_test_name]
                    print 'input'
                    print item[2]
                    final_index = (e for e in indices if e > mach_index).next()
                    self.labels[final_index].color = (163, 207, 95, 255)
            progress_window.close()
            self.is_not_clicked = 2
            self.confirm_label.text = 'DONE'

        elif 2 * self.width / 7 < x < 5 * self.width / 7 and \
                                                0.25 * self.height / 7 < y < self.height / 7 \
              and self.is_not_clicked == 2:
            self.close()


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        print 'initializing'
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
        pass

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
                                                       ('c3B', (0, 0, 200) * 8))
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
        # #########################################################################
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

            temp_sprite = pyglet.sprite.Sprite(green, x=i * self.width / 7 -
                                                        self.width / 7 / 2,
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
            # print remaining_space[0]
            temp_sprite = pyglet.sprite.Sprite(green, x=self.width / 7 / 2,
                                               y=remaining_space[0] - count * spacing -
                                                 0.5 * spacing)
            temp_sprite.visible = False
            self.unique_test_sprites.append([temp_sprite, temp_sprite.position, [temp_sprite.x + temp_sprite.width,
                                                                                 temp_sprite.y + temp_sprite.height],
                                             item])

            [a.append(False) for a in self.tests_to_submit]
            count += 1
        # ######################################################
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
                selected_tests = {}
                for machine_num in range(0, len(self.tests_to_submit)):
                    selected_tests['RT%s' % str(machine_num + 1)] = \
                        [unique_tests[m] for m in
                         [i for i, x in enumerate(self.tests_to_submit[machine_num]) if x]]

                # print selected_tests
                confirmation_window = ConfirmationWindow(selected_tests, width=700, height=500,
                                                         caption='Please confirm')

            for n in range(0, len(self.machine_sprites)):
                item = self.machine_sprites[n]

                if item[1][0] < x < item[2][0] and item[1][1] < y < item[2][1]:
                    if self.machine_sprites[n][0].visible:
                        # print 'is visible'

                        cycle = False

                    else:
                        # print 'turned on'
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
                    # print self.unique_test_sprites[n][0].visible
                    break

            cycle = False

    def on_resize(self, width, height):
        super(Window, self).on_resize(width, height)


def main():
    print 'creating window'
    authentication_window = AuthenticationWindow(width=500, height=200, caption='please log in')
    # window = Window(width=1000, height=600, caption='QA Submitter v1.1', resizable=True)
    pyglet.app.run()


main()
