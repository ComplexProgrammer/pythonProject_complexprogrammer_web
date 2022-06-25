import googletrans
from googletrans import Translator

translator = Translator()
result = translator.translate('Mitä sinä teet')

print(result.src)
print(result.dest)
print(result.origin)
print(result.text)
print(result.pronunciation)