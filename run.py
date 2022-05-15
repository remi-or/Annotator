from backend import AnnotatorBackend

Img_dir = ''
Ann_dir = ''
Classes = ['']

X = AnnotatorBackend(Img_dir, Ann_dir, Classes)
X.main_loop()