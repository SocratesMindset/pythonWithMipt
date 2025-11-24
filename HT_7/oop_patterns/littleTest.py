from structures.histogram import Hist

h = Hist.read("./data/csv_test.csv")
data = h.get_data()

Hist.write("./data/out.bin", data)
Hist.write("./data/out.txt", data)
Hist.write("./data/out.json", data)
Hist.write("./data/out.csv", data)
