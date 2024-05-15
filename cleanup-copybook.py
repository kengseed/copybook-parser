import datetime
import sys
import pathlib
import os
import shutil

keywords = ["*"]


def getFiles(directory):
    files = [f for f in pathlib.Path(directory).iterdir() if f.is_file()]
    return files


def isCotainBadKeyword(content):
    isBadKeyword = False
    for k in keywords:
        if str(content).find(k) > -1:
            return True

    return isBadKeyword


def moveFile(file, targetDirectory):
    # Create directory is not exist
    directory = os.path.join(file.parent, targetDirectory)
    if not os.path.exists(directory):
        os.mkdir(directory)

    # Move file to target directory
    shutil.move(file, os.path.join(directory, file.name))


def cleanupCopybookLine(directory):
    for f in getFiles(directory):
        writeLines = ["       01  START-RECORD.\n"]

        # Read file content
        with open(f, "r") as fp:
            lines = fp.readlines()

            # Append to file contents if not empty line and not found bad keywords
            for line in lines:
                # Replace first 6 character with empty string
                line = "      " + line[6:] if line[:6] != "" else line
                if (
                    line.strip() != ""
                    and line.strip()[:2] != "01"
                    and not isCotainBadKeyword(line)
                ):
                    writeLines.append(line)

        # Write to new cleanup file
        cleanupFile = os.path.join(f.parent, "_cleanup_" + f.stem + ".cbl")
        with open(cleanupFile, "w") as fp:
            fp.writelines(writeLines)

        # Move file to subfolder "_source-file"
        moveFile(f, "_source-file")


if len(sys.argv) > 1 and sys.argv[1] != "":
    cleanupCopybookLine(sys.argv[1])
    print("Cleanup copybook successful.")
