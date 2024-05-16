import copybook
import pandas as pd
import datetime
import sys
import pathlib
import os


def getFiles(directory):
    files = [f for f in pathlib.Path(directory).iterdir() if f.is_file()]
    return files


def findCopyBookFields(children, data, fieldGroup):
    for field in children:
        if type(field) != copybook.Field:
            print(
                ("FieldLevel: {level}; FieldName: {name}; FieldType: {type}").format(
                    level=field.level, name=field.name, type=type(field)
                )
            )

            name = (
                (fieldGroup + "." + field.name if fieldGroup != "" else field.name)
                if type(field) == copybook.FieldGroup
                else ""
            )
            findCopyBookFields(field.children, data, name)
        else:
            data.append(
                {
                    "Field name": field.name,
                    "Field type": field.datatype,
                    "Field length": field.length,
                    "Field group": fieldGroup,
                    "Field level": field.level,
                    "Redefine target": field.redefine_target,
                    "Start position": field.start_pos,
                }
            )


def extractCopyBookFields(copybookFile):
    data = []
    root = copybook.parse_file(copybookFile)
    findCopyBookFields(root.children, data, "")

    return data


def extractCopyBooksToDirectory(copybookDirectory, csvDirectory):
    for f in getFiles(copybookDirectory):
        # Parse copybook to fields
        copybookFields = extractCopyBookFields(f)

        # Generate file name
        csvFileName = ("{time}_{file}.csv").format(
            time=datetime.datetime.now().strftime("%Y%m%d%H%M%S"), file=f.stem
        )
        csvFilePath = os.path.join(csvDirectory, csvFileName)

        df = pd.DataFrame(copybookFields)
        df.to_csv(csvFilePath, sep=",", header=True, index=False)


if len(sys.argv) > 2 and sys.argv[1] != "" and sys.argv[2] != "":
    extractCopyBooksToDirectory(sys.argv[1], sys.argv[2])
    print("Generated copybook to csv files.")
