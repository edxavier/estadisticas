from kivy.base import runTouchApp
from kivy.lang import Builder

runTouchApp(Builder.load_string('''
ActionBar:
    pos_hint: {'top':1}
    ActionView:
        background_normal: (1,1,1,1)
        use_separator: True
        ActionPrevious:
            title: 'Nicroosoft'
            with_previous: False
        ActionOverflow:
        ActionButton:
            text: 'Btn0'
            icon: 'atlas://data/images/defaulttheme/audio-volume-high'
        ActionButton:
            text: 'Abrir'
        ActionButton:
            text: 'Btn2'
        ActionToggleButton:
            text: 'Graficos'
        ActionGroup:
            text: 'Group1'
            ActionButton:
                text: 'Btn5'
            ActionButton:
                text: 'Btn6'
            ActionButton:
                text: 'Btn7'
'''))