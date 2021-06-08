# Importando as bibliotecas
from tkinter import *
from random import *


class ProgramaPrincipal:
    # Criando a janela do jogo
    def __init__(self):

        self.janela = Tk()
        self.janela.title("1010")
        self.janela.geometry("600x750")
        self.janela.configure(background='#474747')
        self.janela.resizable(False, False)

        self.jogo = Jogo(self)

        self.ultimo_x = None
        self.ultimo_y = None
        self.ultima_visualizacao = []

        self.pontos_label = Label(self.janela, font=("Segoe UI Light", 24), bg="#474747", fg="lightgray")
        self.pontos_label["text"] = "0"
        self.pontos_label.place(x=(300 - self.pontos_label.winfo_width() / 2), y=10)

        self.tela = Canvas(self.janela, width=500, height=500, bg="lightgray", highlightthickness=0)
        self.tela.bind("<Button-1>", self.clique_na_tela)
        self.tela.bind("<Motion>", self.renderizar_visualizacao)
        self.tela.bind("<Leave>", self.remover_ultimos_valores)
        self.tela.place(x=50, y=75)

        self.lose_img = PhotoImage(file='./resources/LoseScreenOverlay.gif')
        self.img = PhotoImage(file='./resources/DragAndDropOverlay.gif')
        self.bc_overlay = PhotoImage(file='./resources/BlockCanvasOverlay.gif')

        self.tela_blocos = Canvas(self.janela, width=500, height=125, bg="lightgray", highlightthickness=0)
        self.tela_blocos.place(x=50, y=525 + 50 + 25)

        self.tela_blocos.create_image(0, 0, image=self.bc_overlay, anchor="nw")
        self.img_id = self.tela.create_image(0, 0, image=self.img, anchor="nw")

        self.jogo.gerar_blocos()
        self.renderizar_blocos_atuais()

        # GUILoseScreen(self.window, self.game, self.lose_img)

        self.janela.mainloop()

    # Criando a seleção de blocos do jogo
    def clique_na_tela(self, event):
        x = int(event.x / 50)
        y = int(event.y / 50)
        if (x < 10) and (y < 10):
            if self.jogo.bloco_selecionado is not None:
                coordinates = self.jogo.bloco_selecionado.coord_array
                if self.jogo.encaixa(x, y, coordinates):
                    self.colocar(x, y, coordinates)
                    block = self.jogo.bloco_selecionado
                    block.destruir()
                    self.jogo.bloco_selecionado = None
                    self.jogo.blocos_atuais.remove(block)
                    if len(self.jogo.blocos_atuais) == 0:
                        self.jogo.gerar_blocos()
                        self.renderizar_blocos_atuais()

            if len(self.jogo.checar_linhas()) > 0:
                for lines in self.jogo.checar_linhas():
                    self.jogo.limpar_linha(lines)
                    for i in range(0, 10):
                        self.limpar_coordenadas(i, lines)

            if len(self.jogo.checar_colunas()) > 0:
                for columns in self.jogo.checar_colunas():
                    self.jogo.limpar_coluna(columns)
                    for i in range(0, 10):
                        self.limpar_coordenadas(columns, i)

            if not self.jogo.is_action_possible():
                GUILoseScreen(self.janela, self.jogo, self.lose_img)

    # Visualização
    def renderizar_visualizacao(self, event):
        x = int(event.x / 50)
        y = int(event.y / 50)
        if self.ultimo_x != x or self.ultimo_y != y:
            self.ultimo_x = x
            self.ultimo_y = y
            if self.jogo.bloco_selecionado is not None:
                if 0 <= x and 0 <= y and x < 10 and y < 10:
                    if self.jogo.encaixa(x, y, self.jogo.bloco_selecionado.coord_array):
                        for index in range(0, len(self.ultima_visualizacao)):
                            lx = self.ultima_visualizacao[index][0]
                            ly = self.ultima_visualizacao[index][1]
                            if self.jogo.field[ly][lx] == 0:
                                self.desenhar(self.ultima_visualizacao[index][0], self.ultima_visualizacao[index][1],
                                              "lightgray")
                        if self.jogo.bloco_selecionado is not None:
                            ca = self.jogo.bloco_selecionado.coord_array
                            self.ultima_visualizacao = []
                            for index in range(0, len(ca)):
                                tx = x + ca[index][0]
                                ty = y + ca[index][1]
                                if tx < 10 and ty < 10:
                                    self.desenhar(tx, ty, "yellow")
                                    self.ultima_visualizacao.append([x + ca[index][0], y + ca[index][1]])

    # Colar as peças no lugar desejado
    def colocar(self, x, y, coordinates):
        for index in range(0, len(coordinates)):
            self.desenhar_nas_coordenadas(x + coordinates[index][0], y + coordinates[index][1])
            self.jogo.set_filed(x + coordinates[index][0], y + coordinates[index][1], 1)

    # Remover as linhas completas
    def remover_ultimos_valores(self, event):
        self.ultimo_x = None
        self.ultimo_y = None
        for index in range(0, len(self.ultima_visualizacao)):
            lx = self.ultima_visualizacao[index][0]
            ly = self.ultima_visualizacao[index][1]
            if self.jogo.field[ly][lx] == 0:
                self.desenhar(self.ultima_visualizacao[index][0], self.ultima_visualizacao[index][1], "lightgray")

    # Mudando de cor
    def desenhar_nas_coordenadas(self, x, y):
        self.desenhar(x, y, "orange")

    # Mudando de cor
    def limpar_coordenadas(self, x, y):
        self.desenhar(x, y, "lightgray")

    # Desenhando
    def desenhar(self, x, y, color):
        x = x * 50
        y = y * 50
        self.tela.create_rectangle(x, y, x + 50, y + 50, fill=color, outline="")
        self.restaurar_grade(self.img_id)

    # Renderizando os blocos colocados
    def renderizar_blocos_atuais(self):
        for index in range(0, len(self.jogo.blocos_atuais)):
            c = self.jogo.blocos_atuais[index].obter_tela_de_bloco()
            c.place(x=50 + 166 * (index + 1) - 83 - int(c["width"]) / 2,
                    y=75 + 500 + 25 + (62 - int(c["height"]) / 2))

    # Resetando a grade
    def restaurar_grade(self, img_id):
        self.img_id = self.tela.create_image(0, 0, image=self.img, anchor="nw")
        self.tela.delete(img_id)


class GUILoseScreen:
    def __init__(self, window, game, lose_img):
        canvas = Canvas(window, width=600, height=725, bg="#474747", highlightthickness=0)
        canvas.create_image(0, 0, image=lose_img, anchor="nw")
        canvas.place(x=0, y=0)


class Jogo:
    # Criando a grade com uma matriz
    def __init__(self, gui):
        self.gui = gui
        self.field = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.pontos = 0
        self.blocos = BLOCOS()
        self.blocos_atuais = []
        self.bloco_selecionado = None

    # Checar as linhas
    def checar_linhas(self):
        linhas = []
        for linha in range(0, 10):
            flag = 1
            for i in range(0, 10):
                if self.field[linha][i] != 1:
                    flag = 0
                    break
            if flag == 1:
                linhas.append(linha)
        return linhas

    # Checar as colunas
    def checar_colunas(self):
        colunas = []
        for coluna in range(0, 10):
            flag = 1
            for i in range(0, 10):
                if self.field[i][coluna] != 1:
                    flag = 0
                    break
            if flag == 1:
                colunas.append(coluna)
        return colunas

    # Obter os pontos
    def get_points(self):
        return self.pontos

    # Adicionando os pontos
    def adicionar_pontos(self, pontos):
        self.pontos += pontos
        self.gui.pontos_label["text"] = str(self.pontos)
        self.gui.pontos_label.place(x=(300 - self.gui.pontos_label.winfo_width() / 2), y=10)

    # Limpar as linhas prenchidas
    def limpar_linha(self, index):
        for i in range(0, 10):
            self.set_filed(i, index, 0)

    # Limpar as colunas prenchidas
    def limpar_coluna(self, index):
        for i in range(0, 10):
            self.set_filed(index, i, 0)

    def set_filed(self, x, y, full):
        self.adicionar_pontos(1)
        self.field[y][x] = full

    # Gerando blocos
    def gerar_blocos(self):
        self.blocos_atuais = []
        for i in range(0, 3):
            self.blocos_atuais.append(Bloco(randint(0, len(self.blocos.block_list) - 1), self.blocos, self.gui))

    # Verificando se o bloco se encaixa
    def encaixa(self, x, y, coordinates):
        for index in range(0, len(coordinates)):
            tx = x + coordinates[index][0]
            ty = y + coordinates[index][1]

            if 0 <= tx < 10 and 0 <= ty < 10:
                if self.field[ty][tx] == 1:
                    return False
            else:
                return False
        return True

    # Verificar a possibilidade de ação
    def is_action_possible(self):
        for y in range(0, len(self.field)):
            for x in range(0, len(self.field[y])):
                for block in self.blocos_atuais:
                    if self.encaixa(x, y, block.coord_array):
                        return True
        return False


class Bloco:
    def __init__(self, block_list_index, blocks, gui):
        self.block_list_index = block_list_index
        self.coord_array = blocks.block_list[block_list_index]
        self.gui = gui
        self.window = gui.janela
        self.height = 0
        self.width = 0
        self.width_neg = 0
        self.definir_medicao()
        self.canvas = self.__criar_tela_de_bloco()

    # Definindo o tamanho
    def definir_medicao(self):
        width_pos = 0
        width_neg = 0
        height = 0
        for index in range(0, len(self.coord_array)):
            x1 = self.coord_array[index][0] * 25
            y1 = self.coord_array[index][1] * 25

            if x1 >= 0:
                if x1 + 25 > width_pos:
                    width_pos = x1 + 25
            elif x1 * -1 > width_neg:
                width_neg = (x1 * -1)

            if y1 + 25 > height:
                height = y1 + 25
        self.height = height
        self.width = width_pos + width_neg
        self.width_neg = width_neg

    def obter_tela_de_bloco(self):
        return self.canvas

    # Criando a pintura do bloco
    def __criar_tela_de_bloco(self):
        canvas = Canvas(self.window, width=self.width, height=self.height, bg="lightgray", highlightthickness=0)
        canvas.bind("<Button-1>", self.selecionar_bloco)
        for index in range(0, len(self.coord_array)):
            x1 = self.coord_array[index][0] * 25
            y1 = self.coord_array[index][1] * 25
            canvas.create_rectangle(x1 + self.width_neg, y1, x1 + 25 + self.width_neg, y1 + 25, fill="orange",
                                    outline="")

        return canvas

    # Evento de seleção do bloco
    def selecionar_bloco(self, event):
        selected_block = self.gui.jogo.bloco_selecionado
        if selected_block is not None and selected_block is not self:
            selected_block.remover_contorno()
        self.gui.jogo.bloco_selecionado = self
        self.canvas["highlightthickness"] = 1

    #  Evento de apagar o contorno
    def remover_contorno(self):
        self.canvas["highlightthickness"] = 0

    # Evento de eliminação
    def destruir(self):
        self.canvas.destroy()


class BLOCOS:
    # Definindo o tamanho dos blocos
    def __init__(self):
        self.block_list = [
            [[0, 0]],
            [[0, 0], [0, 1], [0, 2], [1, 1]],
            [[0, 0], [1, 0], [2, 0], [2, 1]],
            [[0, 0], [0, 1]],
            [[0, 0], [0, 1], [0, 2]],
            [[0, 0], [0, 1], [1, 1]],
            [[0, 0], [0, 1], [0, 1]],
            [[0, 0], [0, 1], [1, 0], [1, 1]],
            [[0, 0], [0, -1], [-1, 0]],
            [[0, 0], [0, 1], [1, 0], [0, -1], [-1, 0]],
            [[0, 0], [1, 0], [2, 0]],
            [[0, 0], [1, 0], [2, 0], [2, -1]],
            [[0, 0], [1, 0], [2, 0], [1, -1]],
            [[0, 0], [1, 0], [2, 0], [2, -1], [2, -2], [1, -1]],
            [[0, 0], [0, 1]],
        ]


main = ProgramaPrincipal()
