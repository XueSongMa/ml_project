from sys import argv

scripts, filename = argv

txt = open(filename)

print("here's your file {1}:".format(filename))
print(txt.read())