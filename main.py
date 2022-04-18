import csv

import pandas
import matplotlib.pyplot as plt
from PIL import Image


def get_maximum_index(values):
    max_index = 0
    index = 0
    max_value = 0
    for value in values:
        try:
            if float(value) > float(max_value):
                max_index = index
        except:
            pass
        index += 1
    return max_index


def plot_protein(dataset_a, dataset_b, proteine_name):
    filename = './figures/' + "".join(x for x in proteine_name if x.isalnum()) + '.png'

    # get data via loc function by protein name with pandas
    y_values_a = list(list(dataset_a.loc[dataset_a['T: Gene names'] == proteine_name].values)[0])[1:]
    y_values_b = list(list(dataset_b.loc[dataset_b['T: Gene names'] == proteine_name].values)[0])[1:]

    # cast values into flaot
    try:
        y_values_a = [float(x) for x in y_values_a]
        y_values_b = [float(x) for x in y_values_b]
    except Exception as e:
        print("Could not plot Protein {}! Skipping! Reason: ".format(proteine_name))
        print(str(e))
        return

    max_index_a = get_maximum_index(y_values_a)
    max_index_b = get_maximum_index(y_values_b)

    difference = max_index_a - max_index_b

    x = range(0, len(y_values_a))

    plt.plot(x, y_values_a, label="Dataset A")
    plt.plot(x, y_values_b, label="Dataset B")
    plt.xlabel(proteine_name)
    plt.legend()
    plt.savefig(filename, bbox_inches='tight')
    plt.clf()
    return {
        'protein': proteine_name,
        'max_index_a': max_index_a,
        'max_index_b': max_index_b,
        'difference': difference,
        'filename': filename
    }


if __name__ == '__main__':
    log = []
    dataset_a = pandas.read_csv('./data/dataset_a.csv')
    dataset_b = pandas.read_csv('./data/dataset_b.csv')
    proteins = [x for x in list(dataset_a['T: Gene names']) if not pandas.isna(x)]
    for protein in proteins:
        plot_log = plot_protein(dataset_a, dataset_b, protein)
        if plot_log:
            log.append(plot_log)

    print('Figures written to figures folder')

    with open('./output/result.csv', 'w', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=log[0].keys())
        writer.writeheader()
        writer.writerows(log)

    print('Difference file written to output folder (output/result.csv)')

    images = [
        Image.open(f['filename'])
        for f in log
    ]

    converted_images = []
    for image in images:
        converted_images.append(image.convert('RGB'))

    pdf_path = "./output/report.pdf"

    converted_images[0].save(
        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=converted_images[1:]
    )

    print("Report written to " + "output/report.pdf")
