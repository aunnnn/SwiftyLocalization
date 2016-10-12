import datetime
import os
import csv
import json

NOW = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M")
CURRENT_DIR = os.path.dirname(__file__)

def main():
  print "Generating struct for iOS..."
  with open(os.path.join(CURRENT_DIR,"settings.json")) as setting_file:
    setting = json.load(setting_file)

    IN_PATH = setting["IN_PATH"]
    LANG_KEYS = setting["LANG_KEYS"]

    GEN_STRUCT_BASE_PATH = setting["GEN_STRUCT_BASE_PATH"]
    GEN_STRUCT_OUT_PATH = setting["GEN_STRUCT_OUT_PATH"]
    GEN_STRUCT_FILENAME = setting["GEN_STRUCT_FILENAME"]
    GEN_STRUCT_VALUE_RETRIEVAL = setting["GEN_STRUCT_VALUE_RETRIEVAL"]
    GEN_STRUCT_STRUCT_NAME = setting["GEN_STRUCT_STRUCT_NAME"]


    if GEN_STRUCT_BASE_PATH == "currentdir":
      print "Detect currentdir -> \n  " + CURRENT_DIR
      GEN_STRUCT_BASE_PATH = CURRENT_DIR

    struct_path = os.path.join(GEN_STRUCT_BASE_PATH, GEN_STRUCT_OUT_PATH, GEN_STRUCT_FILENAME)
    folder_path = os.path.join(GEN_STRUCT_BASE_PATH, GEN_STRUCT_OUT_PATH)

    if not os.path.exists(folder_path):
      os.makedirs(folder_path)

    fwrite = open(struct_path, 'w')

    for dirname, dirnames, filenames in os.walk(os.path.join(CURRENT_DIR, IN_PATH)):

      fwrite.write("\n\n\n/*  AUTO-GENERATED: {timestamp}  */\n\n".format(timestamp=NOW))
      fwrite.write("struct {0} {{\n".format(GEN_STRUCT_STRUCT_NAME))
      # for each .csv files
      for f in filenames:
        filename, ext = os.path.splitext(f)
        if ext != '.csv':
          continue
        fullpath = os.path.join(dirname, f)
        print 'Localizing: ' + filename + ' ...'

        fwrite.write('\tstruct {0} {{\n'.format(filename))

        with open(fullpath, 'rb') as csvfile:

          reader = csv.reader(csvfile, delimiter=',')

          iterrows = iter(reader);
          next(iterrows) # skip first line (it is header).

          # for each line
          for row in iterrows:
            row_key = row[0].replace(" ", "")
            # comment
            if row_key[:2] == '//':
              continue

            row_values = [row[i+1] for i in range(len(LANG_KEYS))]

              # if any row is empty, skip it!
            if any([value == "" for value in row_values]):
              continue

            full_key = "{domain}_{key}".format(domain=filename, key=row_key)

            fwrite.write('\t\tstatic var {0}: String {{\n'.format(row_key))
            fwrite.write('\t\t\treturn {0}'.format(GEN_STRUCT_VALUE_RETRIEVAL).format(key=full_key) + '\n')
            fwrite.write('\t\t}\n')


        fwrite.write('\t}\n\n') # e.g., home_care

      fwrite.write('}\n') # HSLocalization

    fwrite.close()

  print 'DONE GENERATE STRUCT FOR IOS.'

if __name__ == '__main__':
  main()