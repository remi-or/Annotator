from backend import AnnotatorBackend

Img_dir = ''
Ann_dir = ''
Classes = ['Unknown']
Keys =    ['x']
Labels =  [-1]

X = AnnotatorBackend(Img_dir, Ann_dir, Classes, Keys, Labels)
X.main_loop()