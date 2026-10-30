import json
import os
import argparse
import glob

print(os.getcwd())


def get_json_files(directory):
    return glob.glob(f"{directory}/*.json")


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-d", help="annotated directory", default=".")
    parser.add_argument("-o", help="output file", default="labels.txt")
    args = parser.parse_args()

    labels = set()
    files = get_json_files(args.d)
    print(f"found json file {len(files)}")
    for file in files:
        with open(file) as f:
            data = json.load(f)
            for shape in data["shapes"]:
                labels.add(shape["label"])

    with open(args.o, "w") as f:
        f.write("__ignore__\n")
        for label in labels:
            f.write(label + "\n")

    return


if __name__ == "__main__":
    main()
