from functools import reduce
def map_func(data):
    year, temp = data.split(',')
    return (year, int(temp))
def reduce_func(data_dict, data):
    year, temp = data
    if year in data_dict:
        if temp > data_dict[year]:
            data_dict[year] = temp
    else:
        data_dict[year] = temp
    return data_dict
def max_temperature_by_year(data):
    mapped_data = map(map_func, data)
    reduced_data = reduce(reduce_func, mapped_data, {})
    return reduced_data
data = ["2025,40", "december,42"]
max_temp_by_year = max_temperature_by_year(data)
print("Maximum temperature by year:")
for year, temp in max_temp_by_year.items():
    print(f"{year}: {temp}°C")
