import phonenumbers
from phonenumbers import geocoder, carrier

x = phonenumbers.parse("+998880340801", None)
print(x)
print(geocoder.description_for_number(x, 'en'))
print(carrier.name_for_number(x, "en"))