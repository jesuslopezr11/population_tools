from pathlib import Path
import argparse
import csv

ROW_1 = ["Australia","Austria","Argentina","Hong Kong","India","Japan","Korea, Republic","Taiwan","Belgium","Croatia","Czech Republic","France","Germany","Hungary","Latvia","Lithuania","Middle East",
         "Poland","Russia","Saudi Arabia","Slovakia","Slovenia", "Spain", "Switzerland","United Arab Emirates","Brazil","Central America","Peru","Uruguay"]
ROW_2 = ["Canada","Indonesia","Malaysia","Myanmar","New Zealand","Pakistan","Philippines","Singapore","Thailand","Vietnam","Central Africa","Denmark","Northern Africa","Finland",
         "Eastern Africa","Greece","Iran","Italy","Western Africa","Netherlands","Norway","Portugal","Romania","South Africa","Southern Africa","Sweden","Turkey","United Kingdom","Chile","Colombia","Ecuador","Mexico","Paraguay","Venezuela"]
other_countries = {"Central Africa":["Angola", "Burundi", "Cameroon", "Central African Republic", "Chad", "Equatorial Guinea", "Gabon", "Republic of the Congo", "Rwanda", "Sao Tome and Principe"],
                    "Northern Africa":["Algeria", "Egypt", "Libya", "Morocco", "Mauritania", "Sudan", "Tunisia", "Western Sahara"],
                    "Eastern Africa": ["South Sudan", "Uganda", "Djibouti", "Eritrea", "Ethiopia", "Somalia","Kenya"],
                    "Southern Africa": ["Madagascar", "Mauritius", "Angola", "Botswana", "Comoros", "DR Congo", "Eswatini", "Lesotho", "Malawi", "Mozambique", "Namibia", "Seychelles", "Tanzania", "Zambia", "Zimbabwe"],
                    "Western Africa": ["Benin", "Burkina Faso", "Cabo Verde", "Ivory Coast", "The Gambia", "Ghana", "Guinea-Bissau", "Guinea", "Liberia", "Mali", "Niger", "Nigeria", "Senegal", "Sierra Leone", "Togo"],
                    "Middle East": ["Bahrain", "Cyprus", "Egypt", "Iran", "Iraq", "Israel", "Jordan", "Kuwait", "Lebanon", "Oman", "Palestine", "Qatar", "Syria", "Yemen"],
                    "Central America": ["Guatemala", "El Salvador", "Honduras", "Nicaragua", "Costa Rica", "Panama", "Belize"]}
age_groups = ["15 - 19", "20 - 24", "25 - 29", "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 55"]
years = ["2023"]
pop_data = {"China":{}, "USA":{}, "ROW_1":{}, "ROW_2":{}}
not_included = []
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
            elif country in ROW_1:
                pop_data["ROW_1"][year] += female_population
            elif country in ROW_2:
                pop_data["ROW_2"][year] += female_population
            else:
                for region in other_countries.keys():
                    if country in other_countries[region]:
                        if region in ROW_1:
                            pop_data["ROW_1"][year] += female_population
                        elif region in ROW_2:
                            pop_data["ROW_1"][year] += female_population
                        else:
                            print (country)
                            print (region)
                        break
                else:
                    if country not in not_included:
                        not_included.append(country)


    csv_rowlist = []
    first_row = ["Market"] + years
    csv_rowlist.append(first_row)
    for market in pop_data.keys():
        market_row = [market]
        for year in pop_data[market].keys():
            market_row.append(pop_data[market][year])
        csv_rowlist.append(market_row)
    
    address = "processed_GYN_data.csv"
    with open(address, "w") as file:
        writer = csv.writer(file, dialect='excel')
        for row in csv_rowlist:
            writer.writerow(row)
        file.close()

    print ("This is the list of countries not included in the country segmentation:")
    print(not_included)