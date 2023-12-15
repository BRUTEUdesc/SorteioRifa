#!/usr/bin/env python3

import csv
import curses
import time
import random
import sys

def ler_participantes(caminho_csv):
    with open(caminho_csv, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        lista = []
        for row in reader:
            lista.append((int(row[0]), row[1]))
        return lista

def exibir_interface(stdscr, participantes):

    most_problable_winners = []
    theoretical_win_probability = {}
    freq = {}

    sum_freq = 0
    sum = 0

    for participante in participantes:
        freq[participante[1]] = freq.get(participante[1], 0) + 1
        # print(participante[1], freq[participante[1]])

    for freq_item in freq.items(): 
        sum_freq += freq_item[1]

    for freq_item in freq.items():
        theoretical_win_probability[freq_item[0]] = freq_item[1] / sum_freq * 100
        sum += theoretical_win_probability[freq_item[0]]

    sorted_theoretical_win_probability = sorted(theoretical_win_probability.items(), key=lambda x: x[1], reverse=True)

    for i in range(len(sorted_theoretical_win_probability)):
        most_problable_winners.append(sorted_theoretical_win_probability[i])

    it = 1
    for item in most_problable_winners:
        print(it, item[0], round(item[1], 4))
        it += 1

    if stdscr is None:
        return

    curses.curs_set(0)  # Oculta o cursor
    stdscr.clear()

    # Define a frase
    frase = "Ação entre amigos do WA"

    # Cria a interface em ASCII
    ascii_art = [

"   _____  ____  _____ _______ ______ _____ ____  ",
"  / ____|/ __ \|  __ \__   __|  ____|_   _/ __ \ ",
" | (___ | |  | | |__) | | |  | |__    | || |  | |",
"  \___ \| |  | |  _  /  | |  |  __|   | || |  | |",
"  ____) | |__| | | \ \  | |  | |____ _| || |__| |",
" |_____/ \____/|_|  \_\ |_|  |______|_____\____/ ",
" \n                                    {fa} \n".format(fa=frase)

    ]

    for i, line in enumerate(ascii_art):
        stdscr.addstr(i, 0, line)

    stdscr.refresh()

    # Aguarda a entrada do usuário para iniciar o sorteio
    stdscr.getch()

    used = {}

    try:
        num_premios = 8
        premio = 1
        premios = {
            1: 'RODÍZIO DE PIZZA',
            2: 'RELÓGIO DIGITAL',
            3: 'TORRE DE CHOPP E PORÇÃO TORRE (METROVILLE)',
            4: 'TORRE DE CHOPP E PORÇÃO TORRE (METROVILLE)',
            5: 'CAIXA DE HEINEKEN E BOLSA TÉRMICA',
            6: 'COBRE LEITO KING SIZE',
            7: 'DUPLINHA NECESSAIRE',
            8: '5L DE AÇAÍ'
        }
        ganhadores = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None
        }
        while premio <= num_premios:
            # Sorteio
            stdscr.clear()
            for i, line in enumerate(ascii_art):
                stdscr.addstr(i, 0, line)

            # Simula um atraso para dar a sensação de sorteio
            stdscr.addstr(len(ascii_art) + 2, 2, f"Sorteio do {premio}º prêmio: {premios[premio]}", curses.A_BOLD)
            stdscr.getch()
            stdscr.addstr(len(ascii_art) + 4, 2, "Sorteando...", curses.A_BOLD)
            stdscr.refresh()
            time.sleep(1)

            # Simula um número sorteado
            for i in range(80):
                numero_sorteado = random.randint(1, len(participantes))
                assert numero_sorteado > 0 and numero_sorteado <= len(participantes)
                numero_rifa = participantes[numero_sorteado - 1][0]
                stdscr.addstr(len(ascii_art) + 5, 2, f"Número Sorteado: {numero_rifa:>{4}}", curses.A_BOLD)
                stdscr.refresh()
                time.sleep(0.01)

            numero_sorteado = random.randint(1, len(participantes))
            numero_rifa = participantes[numero_sorteado - 1][0]

            while numero_rifa in used:
                numero_sorteado = random.randint(1, len(participantes))
                numero_rifa = participantes[numero_sorteado - 1][0]

            stdscr.addstr(len(ascii_art) + 5, 2, f"Número Sorteado: {numero_rifa:>{4}}", curses.A_BOLD)
            stdscr.refresh()
            # print(numero_sorteado, numero_rifa, participantes[numero_sorteado - 1])
            used[numero_rifa] = True

            # Obtém o nome do ganhador
            ganhador = participantes[numero_sorteado - 1][1]
            time.sleep(0.6)
            stdscr.addstr(len(ascii_art) + 7, 2, f"Ganhador: {ganhador}", curses.A_BOLD)
            
            ganhadores[premio] = ganhador

            stdscr.refresh()
            # Aguarda a entrada do usuário para continuar
            key = stdscr.getch()
            if key == ord('q'):
                break
            premio += 1
        
        stdscr.clear()

        for i, line in enumerate(ascii_art):
            stdscr.addstr(i, 0, line)
        
        stdscr.addstr(len(ascii_art) + 2, 2, "Ganhadores:", curses.A_BOLD)

        for i in range(1, num_premios + 1):
            stdscr.addstr(len(ascii_art) + 2 + i, 2, f"{i}º prêmio - {premios[i]}: {ganhadores[i]}", curses.A_BOLD)
        
        stdscr.refresh()
        stdscr.getch()

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    caminho_csv = sys.argv[1]
    participantes = ler_participantes(caminho_csv)
    exibir_interface(None, participantes)
    # curses.wrapper(exibir_interface, participantes)
