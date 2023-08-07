from pathlib import Path
import argparse
import csv

age_groups = ["15 - 19", "20 - 24", "25 - 29", "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 54"]
years = ["2029", "2030", "2031", "2032", "2033", "2034", "2035", "2036", "2037", "2038"]
pop_data = {"China":{}, "USA":{}, "ROW":{}}
for region in pop_data.keys():
    for year in years:
        pop_data[region][year] = 0

print(str(pop_data))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="Introduce file path")
    args = parser.parse_args()
    data_file = Path(args.file_path)
    parent_folder = str(data_file.stem)
    read_file = str(open(data_file, "r").read())
    data_lines = read_file.splitlines()

    for line in data_lines[1:]:
        sub_groups = line.split(",")
        country = sub_groups[2].strip('"').strip("'")
        year = sub_groups[3].strip('"').strip("'")
        age = sub_groups[4].strip('"').strip("'")
        female_population = float(sub_groups[9].strip('"').strip("'"))

        if age not in age_groups:
            continue
        else:
            if country == "China":
                pop_data["China"][year] += female_population
            elif country == "United States":
                pop_data["USA"][year] += female_population
            else:
                pop_data["ROW"][year] += female_population


    csv_rowlist = []
    first_row = ["Market"] + years

    csv_rowlist.append(first_row)
    for market in pop_data.keys():
        market_row = [market]
        for year in pop_data[market].keys():
            market_row.append(pop_data[market][year])
        csv_rowlist.append(market_row)

    print (csv_rowlist)
    
    address = "processed_pop_data.csv"
    with open(address, "w") as file:
        writer = csv.writer(file, dialect='excel')
        for row in csv_rowlist:
            writer.writerow(row)
        file.close()