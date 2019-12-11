from General_Components.NameSpaces import *

# To Access a perticular value of a field by its id
class ClsUserDetails():
    def getSpecificField(UsrId, Field):
        Usr = User.objects.filter(id= UsrId)
        a = list(Usr.values())
        return (a[0][Field])

