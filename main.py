from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from relogio import Relogio


class RelogioApp(App):
    def build(self):
        return Interface()


class Interface(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.relogio = Relogio()

        # WIDGET DO BOTÃO DE AJUSTAR
        ajustar = Button(text='Ajustar relógio', size_hint=(0.165, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        ajustar.bind(on_press=self.ajustar_relogio)
        self.add_widget(ajustar)

        mais_hora = Button(text='+', size_hint=(0.05, 0.05), pos_hint={'center_x': 0.39, 'center_y': 0.43})
        mais_hora.bind(on_press=self.modificador_hora)
        self.add_widget(mais_hora)
        menos_hora = Button(text='-', size_hint=(0.05, 0.05), pos_hint={'center_x': 0.39, 'center_y': 0.38})
        menos_hora.bind(on_press=self.modificador_hora)
        self.add_widget(menos_hora)

        mais_minuto = Button(text='+', size_hint=(0.05, 0.05), pos_hint={'center_x': 0.61, 'center_y': 0.43})
        mais_minuto.bind(on_press=self.modificador_minuto)
        self.add_widget(mais_minuto)
        menos_minuto = Button(text='-', size_hint=(0.05, 0.05), pos_hint={'center_x': 0.61, 'center_y': 0.38})
        menos_minuto.bind(on_press=self.modificador_minuto)
        self.add_widget(menos_minuto)

        # WIDGETS DO CRONOMETRO
        crono = Button(text='Iniciar cronômetro', size_hint=(0.165, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.2})
        crono.bind(on_press=self.cronometro)
        self.add_widget(crono)
        self.parar = Button(text='Parar', size_hint=(0.1, 0.08), pos_hint={'center_x': 0.65, 'center_y': 0.2},
                            background_color=(1, 0, 0, 1))
        self.parar.bind(on_press=self.parar_cronometro)
        self.flag_parar = False
        self.buffer = 0
        self.volta = Button(text='Volta', size_hint=(0.1, 0.08), pos_hint={'center_x': 0.35, 'center_y': 0.2},
                            background_color=(0, 0, 1, 1))
        self.volta.bind(on_press=self.volta_cronometro)
        self.flag_volta = False
        self.lista_voltas = []

        # WIDGETS PARA O TEMPORIZADOR
        temporizador = Button(text='Temporizador', size_hint=(0.165, 0.08),
                                   pos_hint={'center_x': 0.5, "center_y": 0.1}, background_color=(1, 1, 0, 1))
        temporizador.bind(on_press=self.iniciar_temp)
        self.add_widget(temporizador)

        # WIDGETS PARA AJUSTAR AS HORAS
        self.label_hora = Label(text='HORA', size_hint=(0.5, 0.5), pos_hint={'center_x': 0.45, 'center_y': 0.45})
        self.add_widget(self.label_hora)
        self.hora_input = TextInput(text="0", multiline=False, size_hint=(0.05, 0.05), readonly=True,
                                    pos_hint={'center_x': 0.45, 'center_y': 0.4})
        self.hora_input.bind(on_text_validate=self.relogio.ajustar_hora)
        self.add_widget(self.hora_input)

        # WIDGETS PARA AJUSTAR OS MINUTOS
        self.label_minuto = Label(text='MINUTO', size_hint=(0.5, 0.5), pos_hint={'center_x': 0.55, 'center_y': 0.45})
        self.add_widget(self.label_minuto)
        self.minuto_input = TextInput(text="0", multiline=False, size_hint=(0.05, 0.05), readonly=True,
                                      pos_hint={'center_x': 0.55, 'center_y': 0.4})
        self.minuto_input.bind(on_text_validate=self.relogio.ajustar_minuto)
        self.add_widget(self.minuto_input)

        # WIDGET DO RELÓGIO
        self.modo = Label(text='---', size_hint=(0.5, 0.5), font_size=30,
                          pos_hint={'center_x': 0.5, 'center_y': 0.79})
        self.add_widget(self.modo)
        self.label_relogio = Label(text='00:00:00', font_size=40, size_hint=(0.5, 0.5),
                                   pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.add_widget(self.label_relogio)

        # WIDGET INDICATIVA DE ERRO
        self.label_suporte = Label(text='', font_size=30, size_hint=(0.5, 0.5),
                                   pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.add_widget(self.label_suporte)

    def cancelar_eventos(self):
        Clock.unschedule(self.atualizar_label_relogio)
        Clock.unschedule(self.atualizar_cronometro)
        Clock.unschedule(self.atualizar_temporizador)

    def modificador_hora(self, instance):
        if instance.text == "+":
            numero = int(self.hora_input.text) + 1
            if numero == 13:
                numero = 1
            self.hora_input.text = str(numero)
        if instance.text == "-":
            numero = int(self.hora_input.text) - 1
            if numero == -1:
                numero = 12
            self.hora_input.text = str(numero)

    def modificador_minuto(self, instance):
        if instance.text == "+":
            numero = int(self.minuto_input.text) + 1
            if numero == 60:
                numero = 0
            self.minuto_input.text = str(numero)
        if instance.text == "-":
            numero = int(self.minuto_input.text) - 1
            if numero == -1:
                numero = 59
            self.minuto_input.text = str(numero)

    def ajustar_relogio(self, instance):
        self.modo.text = "Relógio"
        self.relogio.ajustar_hora(self.hora_input)
        self.relogio.ajustar_minuto(self.minuto_input)
        self.cancelar_eventos()
        self.label_relogio.text = f'{self.relogio.hora}:{self.relogio.minuto}:00'
        self.relogio.contador = 0
        Clock.schedule_interval(self.atualizar_label_relogio, 1)

    def atualizar_label_relogio(self, dt):
        self.label_relogio.text = self.relogio.iniciar_relogio()

    def atualizar_cronometro(self, dt):
        self.label_relogio.text = self.relogio.cronometro(buffer=self.buffer)

    def atualizar_temporizador(self, dt):
        self.label_relogio.text = self.relogio.temporizador()
        if self.label_relogio.text == "Fim":
            Clock.unschedule(self.atualizar_temporizador)
            SoundLoader.load("alarme.mp3").play()

    def cronometro(self, instance):
        self.parar.background_color = (1, 0, 0, 1)
        self.buffer = 0
        Clock.unschedule(self.atualizar_label_relogio)
        Clock.unschedule(self.atualizar_temporizador)
        if self.flag_parar:
            self.remove_widget(self.parar)
        self.add_widget(self.parar)
        if self.flag_volta:
            self.remove_widget(self.volta)
        self.add_widget(self.volta)
        self.flag_volta = True
        self.flag_parar = True
        self.parar.text = "Parar"
        self.modo.text = "Cronômetro"
        self.relogio.resetar_parametros()
        self.relogio.iniciar_cronometro()
        Clock.schedule_interval(self.atualizar_cronometro, 0.01)

    def parar_cronometro(self, instance):
        if self.parar.text == "Retomar":
            self.relogio.iniciar_cronometro()
            Clock.schedule_interval(self.atualizar_cronometro, 0.01)
            self.parar.text = "Parar"
            self.parar.background_color = (1, 0, 0, 1)
        else:
            self.buffer = self.relogio.tempo_decorrido
            Clock.unschedule(self.atualizar_cronometro)
            self.parar.text = "Retomar"
            self.parar.background_color = (0, 1, 0, 1)

    def volta_cronometro(self, instance):
        self.lista_voltas.append(self.relogio.tempo_decorrido)
        self.label_suporte.text = self.relogio.cronometro(self.lista_voltas[-1], volta=True)

    def iniciar_temp(self, instance):
        self.modo.text = "Temporizador"
        self.relogio.ajustar_hora(self.hora_input)
        self.relogio.ajustar_minuto(self.minuto_input)
        self.cancelar_eventos()
        self.label_relogio.text = f'{self.relogio.hora}:{self.relogio.minuto}:00'
        self.relogio.contador = 0
        Clock.schedule_interval(self.atualizar_temporizador, 1)


if __name__ == '__main__':
    RelogioApp().run()
