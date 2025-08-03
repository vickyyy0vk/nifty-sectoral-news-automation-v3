import json

DATA_FILE = 'nse_sectoral_data.json'
JS_FILE = 'nse_data_updater.js'
JS_VAR_NAME = 'nseSectoralNewsData'

def main():
    with open(DATA_FILE, 'r') as fin:
        data = json.load(fin)
    with open(JS_FILE, 'w') as fout:
        fout.write(f"const {JS_VAR_NAME} = ")
        json.dump(data, fout, indent=2)
        fout.write(";")

if __name__ == "__main__":
    main()
