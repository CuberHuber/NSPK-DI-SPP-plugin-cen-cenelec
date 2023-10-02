
from cen_cenelec import CEN_CENELEC


parser = CEN_CENELEC()

docs = parser.content()

print(docs)