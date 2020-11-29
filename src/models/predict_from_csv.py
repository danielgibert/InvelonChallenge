import argparse
import csv
import sys
sys.path.append("../../")
from src.models.predict_from_stl import predict
import numpy as np

def predict_from_csv(model_filepath, csv_filepath, output_filepath, width=480, height=640):
    """
    Predicts the category of the test samples given in a csv file
    :param model_filepath: str
    :param csv_filepath: str
    :param width: int
    :param height: int
    :return: None
    """
    correct_classifications = 0
    incorrect_classifications = 0
    with open(output_filepath, "w") as output_file:
        with open(csv_filepath, "r") as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=["filename", "ID"])
            reader.__next__()
            for row in reader:
                print(row["filename"], row['ID'], np.argmax())
                predictions = predict(model_filepath, row["filename"], width, height)
                output_file.write("{},{},{}\n".format(row['filename'], predictions), row['ID'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to predict from jpeg')
    parser.add_argument("model_filepath",
                        type=str,
                        help="Model filepath")
    parser.add_argument("csv_filepath",
                        type=str,
                        help="CSV filepath")
    parser.add_argument("output_filepath",
                        type=str,
                        help="Output filepath")
    parser.add_argument("--width",
                        type=int,
                        help="Width of the images",
                        default=480)
    parser.add_argument("--height",
                        type=int,
                        help="Height of the images",
                        default=640)
    args = parser.parse_args()

    predict_from_csv(args.model_filepath, args.csv_filepath, args.output_filepath, args.width, args.height)
