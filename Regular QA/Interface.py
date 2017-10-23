import pyglet
window = pyglet.window.Window()
label = pyglet.text.Label('QA submission',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center', height= window.height)
@window.event
def on_draw():
    window.clear()
    label.draw()

pyglet.app.run()