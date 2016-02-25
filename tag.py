
import json
from subprocess import call
# read json file
with open('current_playlist.json') as data_file:
    data = json.load(data_file)

#print(data["A"]["1"]["path"])

# read tex file
f = open("latex/tag.tex", "r")
contents = f.readlines()

index = 0
for line in contents:
    index += 1
    if("\\begin{document}" in line):
        break
print ("index " + str(index))
f.close()

for var in range(10):
    contents.insert(index, "Toto et Tata\n")
    index += 1


contents.insert(index, "\end{document}\n")

contents = contents[:index+1]
f = open("latex/tag.tex", "w")
f.writelines(contents)
f.close()

b = True
letters = ['A', 'B', 'C', 'D']
numbers = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']

# for letter in letters:
#     for number in numbers:
#         if(b):
#             line = "\\boite{\content{%s}{%s}{%s}}" % (letter+number,data[letter][number]["title"],data[letter][number]["artist"])
#             b = False
#
#         else:
#             line += "{\content{%s}{%s}{%s}}\n" % (letter+number,data[letter][number]["title"],data[letter][number]["artist"])
#             b= True
#             contents.insert(index, line)
#             index += 1
#
#
# f = open("latex/tag.tex", "w")
# f.writelines(contents)
# f.close()


# generate pdf file in latex directory: latex/tag.pdf
#call(["pdflatex","-output-directory", "latex/","latex/tag.tex"])
