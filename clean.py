import csv
import argparse

def processa_csv(input_path):
    with open(input_path, 'r', newline='', encoding='utf-8') as input_file:
        output_path = input_path[:-4] + '_clean.csv'

        with open(output_path, 'w', newline='', encoding='utf-8') as output_file:
            reader = csv.reader(input_file, delimiter=',')
            writer = csv.writer(output_file, delimiter=',')

            for row in reader:
                if row[0].isdigit() and len(row[1]) > 0:
                    writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description='Processa um arquivo CSV removendo linhas que não começam com números e números que não foram vendidos.')
    parser.add_argument('input_path', help='Caminho do arquivo CSV de entrada')

    args = parser.parse_args()
    processa_csv(args.input_path)

if __name__ == '__main__':
    main()

