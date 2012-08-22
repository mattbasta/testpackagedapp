import random


words = ["roardtenarin", "housbonunshi", "pondwioxer", "tuourdwig",
         "clastsordbenver", "moundetmak", "nerthocylfon", "trapourin",
         "slilstwhoomre", "malcal", "acrandmeasent", "telbatwhim",
         "adealor", "gemastac", "plagtatill", "mezomcusings", "ousmemy",
         "hawshansperif", "ovtucout", "bluesatba", "hispo", "ivafu", "cyca",
         "yleri", "halfanan", "plamapcasnem", "bogiki", "broardbaspled",
         "sapdoswind", "bagrar", "tookchande", "ererly", "idotilant",
         "didhu", "blesuscri", "pencout", "headinphy", "itnowing", "io",
         "abertirym", "ereaser", "shadtomcon", "bipostred", "floonlyl",
         "illkight", "frioldfa", "necspeedne", "futmastbubtiz", "ethsci",
         "prophgrannacack", "messishapov", "cuowblelpen", "rincal",
         "britonzontack", "omcunmane", "atsusheco", "lievingtant",
         "entquarver", "enellwa", "ightlyterock", "crousdowgrist",
         "dispeent", "exingchar", "mentru", "fernewcrizsam", "thimartse",
         "aclivtournban", "earicesy"]


def _word():
   return random.choice(words)


def generate_id():
    return "%s_%s%d" % (_word(), _word(), random.randint(0, 1000))


def _cap(word):
   return word[0].upper() + word[1:]


def generate_name():
   name = [_cap(_word()) for i in range(3)]
   return " ".join(name)


def generate_description():
   desc = [_word() for i in range(15)]
   desc[0] = _cap(desc[0])
   return "%s." % " ".join(desc)
