import math
import random
import tkinter as tk
from tkinter import ttk, messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox


def ler_nomes_do_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, "r") as arquivo:
            nomes = [linha.strip() for linha in arquivo.readlines()]
        return nomes
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
        return []


class TercoEscalaApp:
    def __init__(self, _root):
        self.tabela_nomes = None
        self.dropdown_nome = None
        self.dropdown_dia = None
        self.root = root
        self.root.title("Agenda")

        # Lista de dias da semana
        self.dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

        # Lista de nomes lidos do arquivo
        self.nomes = ler_nomes_do_arquivo("nomes.txt")
        self.num_max_pessoas_por_dia = math.ceil(len(self.nomes)/len(self.dias_semana))
        self.num_min_pessoas_por_dia = math.floor(len(self.nomes)/len(self.dias_semana))
        # criar dicionario dos dias da semana
        self.terco_semanal = {dia: set() for dia in self.dias_semana}

        # Variáveis para armazenar a seleção
        self.dia_selecionado = tk.StringVar()
        self.nome_selecionado = tk.StringVar()

        # Criar e posicionar os widgets
        self.criar_widgets()

    def criar_widgets(self):
        # Dropdown para os dias da semana
        label_dia = tk.Label(self.root, text="Selecione o Dia:")
        label_dia.pack(pady=10)
        self.dropdown_dia = AutocompleteCombobox(self.root, completevalues=self.dias_semana,
                                                 textvariable=self.dia_selecionado)
        self.dropdown_dia.pack(pady=10)

        # Dropdown para os nomes lidos do arquivo
        label_nome = tk.Label(self.root, text="Selecione o Nome:")
        label_nome.pack(pady=10)
        self.dropdown_nome = AutocompleteCombobox(self.root, completevalues=self.nomes,
                                                  textvariable=self.nome_selecionado)
        self.dropdown_nome.pack(pady=10)

        # Botão de confirmação
        botao_confirmar = tk.Button(self.root, text="Confirmar", command=self.confirmar_nome)
        botao_confirmar.pack(pady=20)

        # Botão de randomizar
        botao_randomizar = tk.Button(self.root, text="Randomizar", command=self.randomizar_nome)
        botao_randomizar.pack(pady=20)

        # Tabela para mostrar os nomes por dia da semana
        self.tabela_nomes = ttk.Treeview(self.root, columns=self.dias_semana, show="headings", height=5)
        for dia in self.dias_semana:
            self.tabela_nomes.heading(dia, text=dia)
            self.tabela_nomes.column(dia, width=60, anchor='center')

        # Preencher a tabela inicialmente
        self.atualizar_tabela()

        self.tabela_nomes.pack(pady=20)

    def confirmar_nome(self):
        dia = self.dia_selecionado.get()
        nome = self.nome_selecionado.get()

        if dia and nome:
            self.terco_semanal[dia].add(nome)
            self.nomes.remove(nome)

            # Atualizar os valores do dropdown e a tabela

            self.atualizar_tabela()
            self.verificar_se_dia_esta_cheio(dia)
            self.atualizar_dropdowns()

        else:
            messagebox.showwarning("Aviso", "Por favor, selecione um dia e um nome.")

    def verificar_se_dia_esta_cheio(self, dia):
        if len(self.terco_semanal[dia]) == self.num_max_pessoas_por_dia:
            if self.num_max_pessoas_por_dia > self.num_min_pessoas_por_dia:
                self.num_max_pessoas_por_dia = self.num_max_pessoas_por_dia - 1
            self.dias_semana.remove(dia)

    def randomizar_nome(self):
        while len(self.nomes) != 0:
            dia_aleatorio = random.choice(self.dias_semana)
            if len(self.terco_semanal[dia_aleatorio]) < self.num_max_pessoas_por_dia:
                nome_aleatorio = random.choice(self.nomes)
                self.terco_semanal[dia_aleatorio].add(nome_aleatorio)
                self.nomes.remove(nome_aleatorio)
                self.verificar_se_dia_esta_cheio(dia_aleatorio)

        self.atualizar_tabela()

    def atualizar_dropdowns(self):
        # Atualizar valores do dropdown de dias da semana
        self.dia_selecionado.set("")
        self.dropdown_dia.set_completion_list(self.dias_semana)

        # Atualizar valores do dropdown de nomes
        self.nome_selecionado.set("")
        self.dropdown_nome.set_completion_list(self.nomes)

    def atualizar_tabela(self):
        # Limpar a tabela
        for i in self.tabela_nomes.get_children():
            self.tabela_nomes.delete(i)

        self.preencher_tabela()
        # Adicionar dados à tabela
        self.adicionar_na_tabela()

    def preencher_tabela(self):
        # Insere linhas vazias na Treeview
        for i in range(0, 5):
            self.tabela_nomes.insert('', i, text='')

    def adicionar_na_tabela(self):
        # Adicionar nomes diretamente nas colunas correspondentes
        for dia, nomes_dia in self.terco_semanal.items():
            coluna_index = list(self.terco_semanal.keys()).index(dia)
            for i, nome in enumerate(nomes_dia):
                # Pega a id da linha
                linha_id = self.tabela_nomes.get_children()[i]

                # Atualiza a linha com o nome do dia específico
                self.tabela_nomes.set(linha_id, coluna_index, nome)


# Criar a janela principal
root = tk.Tk()
app = TercoEscalaApp(root)

# Iniciar o loop de eventos
root.mainloop()
