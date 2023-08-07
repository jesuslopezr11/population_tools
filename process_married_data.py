from pathlib import Path
import argparse
import csv

age_groups = ["15-49"]
years = ["2029", "2030"]
pop_data = {"China":{}, "USA":{}, "ROW":{}}
clean = {"China":{}, "USA":{}, "ROW":{}}


if __name__ == "__main__":

    for region in pop_data.keys():
        if region != "ROW":
            for year in years:
                pop_data[region][year] = 0
        else:
            for year in years:
                pop_data[region][year]= {}
    
    for region in clean.keys():
        for year in years:
            clean[region][year] = 0

    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="Introduce file path")
    args = parser.parse_args()
    data_file = Path(args.file_path)
    read_file = str(open(data_file, "r").read())
    data_lines = read_file.splitlines()

    for line in data_lines[1:]:
        sub_groups = line.split(",")
        if len(sub_groups) == 8:
            country = sub_groups[0]
            year = sub_groups[3]
            age = sub_groups[4]
            female_population = float(sub_groups[6])
            percentage = float(sub_groups[5])
        elif len (sub_groups) == 9:
            try:
                check = int(sub_groups[1])
                if type(check) is int:
                    country = sub_groups[0]
                    year = sub_groups[3]
                    age = sub_groups[4]
                    female_population1 = str(sub_groups[6].strip('"'))
                    female_population2 = str(sub_groups[7].strip('"'))
                    female_population = float(female_population1 + female_population2)
                    percentage = float(sub_groups[5])
                else:
                    print("It was not an integer")
            except:
                country = sub_groups[1].strip('"')
                year = sub_groups[4]
                age = sub_groups[5]
                female_population = float(sub_groups[7])
                percentage = float(sub_groups[6])
        else:
            if len(sub_groups) == 10:
                country = sub_groups[1].strip('"')
                year = sub_groups[4]
                age = sub_groups[5]
                percentage = float(sub_groups[6])
                female_population1 = str(sub_groups[7].strip('"'))
                female_population2 = str(sub_groups[8].strip('"'))
                female_population = float(female_population1 + female_population2)
            else:
                print ("Houston we have a problem")

        if year not in years:
            continue
        else:
            if age not in age_groups:
                continue
            else:
                if country == "China":
                    pop_data["China"][year] = percentage
                    clean["China"][year] = percentage
                elif country == "United States of America":
                    pop_data["USA"][year] = percentage
                    clean["USA"][year] = percentage
                else:
                    pop_data["ROW"][year][country]= {"percentage":percentage, "number":female_population}

    for year in pop_data["ROW"].keys():
        total = 0.0
        apportion = 0.0
        for country in pop_data["ROW"][year].keys():
            total += pop_data["ROW"][year][country]["number"]
            apportion += (pop_data["ROW"][year][country]["number"] * (pop_data["ROW"][year][country]["percentage"] / 100.0))
        average = float (apportion / total)
        clean["ROW"][year] = average

    csv_rowlist = []
    first_row = ["Market"] + years
    csv_rowlist.append(first_row)
    for market in clean.keys():
        market_row = [market]
        for year in clean[market].keys():
            market_row.append(clean[market][year])
        csv_rowlist.append(market_row)
    
    address = "processed_married_data.csv"
    with open(address, "w") as file:
        writer = csv.writer(file, dialect='excel')
        for row in csv_rowlist:
            writer.writerow(row)
        file.close()