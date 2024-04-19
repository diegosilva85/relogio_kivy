import time


class Relogio:
    def __init__(self):
        self.hora_int = None
        self.minuto_int = None
        self.contador = 0
        self.segundo = "00"
        self.hora = None
        self.minuto = None
        self.contador_cronometro = 0
        self.milisegundo = 0
        self.tempo_inicial = 0
        self.tempo_decorrido = 0

    def ajustar_hora(self, instance):
        self.hora_int = int(instance.text)
        self.hora = self.display(self.hora_int)
        # try:
        #     self.hora_int = int(instance.text)
        #     if self.hora_int > 23 or self.hora_int < 0:
        #         self.hora = "erro"
        #     else:
        #         self.hora = self.display(self.hora_int)
        # except ValueError:
        #     self.hora = "erro"

    def ajustar_minuto(self, instance):
        self.minuto_int = int(instance.text)
        self.minuto = self.display(self.minuto_int)
        # try:
        #     self.minuto_int = int(instance.text)
        #     if self.minuto_int > 59 or self.minuto_int < 0:
        #         self.minuto = "erro"
        #     else:
        #         self.minuto = self.display(self.minuto_int)
        # except ValueError:
        #     self.minuto = "erro"

    def display(self, valor: int) -> str:
        if valor < 10:
            return f'0{valor}'
        if valor >= 10:
            return f'{valor}'

    def iniciar_relogio(self) -> str:
        self.contador += 1
        if self.contador == 60:
            self.minuto_int += 1
            self.contador = 0
        if self.minuto_int == 60:
            self.hora_int += 1
            self.minuto_int = 0
        if self.hora_int == 24:
            self.hora_int = 0

        self.segundo = self.display(self.contador)
        self.minuto = self.display(self.minuto_int)
        self.hora = self.display(self.hora_int)

        return f'{self.hora}:{self.minuto}:{self.segundo}'

    def cronometro(self, buffer, volta=False) -> str:
        if not volta:
            self.tempo_decorrido = time.time() - self.tempo_inicial + buffer
        else:
            self.tempo_decorrido = buffer
        self.hora_int = int(self.tempo_decorrido / 3600)
        self.tempo_decorrido %= 3600
        self.minuto_int = int(self.tempo_decorrido / 60)
        self.tempo_decorrido %= 60
        self.contador = int(self.tempo_decorrido)
        self.contador_cronometro = int((self.tempo_decorrido - self.contador) * 100)

        self.milisegundo = self.display(self.contador_cronometro)
        self.segundo = self.display(self.contador)
        self.minuto = self.display(self.minuto_int)
        self.hora = self.display(self.hora_int)

        return f'{self.hora}:{self.minuto}:{self.segundo}.{self.milisegundo}'

    def iniciar_cronometro(self):
        self.tempo_inicial = time.time()

    def temporizador(self):
        if self.hora_int != 0:
            if self.minuto_int == 0 and self.contador == 0:
                self.hora_int -= 1
                self.minuto_int = 59
                self.contador = 60
            elif self.contador == 0:
                self.minuto_int -= 1
                self.contador = 60
            self.contador -= 1
        else:
            if self.contador == 0:
                self.minuto_int -= 1
                self.contador = 60

            self.contador -= 1

            if self.minuto_int == 0:
                if self.contador == 0:
                    return 'Fim'
        self.segundo = self.display(self.contador)
        self.minuto = self.display(self.minuto_int)
        self.hora = self.display(self.hora_int)

        return f'{self.hora}:{self.minuto}:{self.segundo}'

    def resetar_parametros(self):
        self.hora_int = 0
        self.minuto_int = 0
        self.contador_cronometro = 0
        self.contador = 0
        self.milisegundo = 0
