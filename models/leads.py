from mongoengine import DynamicDocument, ImageField, StringField, ValidationError, PointField
from database.db_connection import client_orm


def validate_name(lead_name):
    if Leads.objects(lead_name=lead_name):
        raise ValidationError


def validate_type(lead_type):
    if Leads.objects(lead_type=lead_type):
        raise ValidationError


class Leads(DynamicDocument):
    username = StringField(min_length=4, max_length=30, required=True)
    name = StringField(min_length=4, max_length=25, required=True)
    type = StringField(min_length=4, max_length=15, required=True)
    image = ImageField()

# ------------LOCATION DOCUMENTATION-------------
# https://stackoverflow.com/questions/61665669/how-to-store-location-in-point-field-using-mongo-engine-and-fetch-nearest-5-rest
# from geojson import Point
# location = Point((Decimal(lat), Decimal(lon)))
# -----------------------------------------------


# --------------IMAGE DOCUMENTATION---------------
# https://groups.google.com/g/mongoengine-users/c/n_cITLxpihg
# https://www.youtube.com/watch?v=PO-z4nwdMUs
# photo = photo.convert('L') #CONVERTS TO GRAYSCALE
# photo.save('aragorn1.png') #SAVES THE GRAYSCALE PHOTO
# ------------------------------------------------


# def post(self, *args, **kwargs):
#     merchant = self._merchant
#     data = self._data
#     obj_data = {}
#     if merchant:
#         params = self.serialize() # I am getting params dict. NO Issues with this.
#         obj_data['name'] = params.get('title', None)
#         obj_data['description'] = params.get('description', None)
#         path = params.get('file_path', None)
#         image = Image.open(path)
#         print image # **
#         obj_data['image'] = image # this is also working fine.
#         obj_data['caption'] = params.get('caption', None)
#         obj_data['user'] = user
#         des = Description(**obj_data)
#         des.save()
#
#         print obj_data['image'] # **
#         print des.image # This is printing as <ImageGridFsProxy: None>
#
#         des = Description()
#         des.image.put(open(params.get('file_path', None)))
#         des.save()
