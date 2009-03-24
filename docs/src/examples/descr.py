from scikits.samplerate import available_convertors, convertor_description

for type in available_convertors():
    print convertor_description(type)
