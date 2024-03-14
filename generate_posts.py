# HOW TO USE:
# 1. Run 'pip install exif'
# 2. Place a folder of images with coordinate metadata in media/post_photos
# 3. Run 'python manage.py shell'
# 4. 'import generatePosts'
# 5. 'generate_posts.generate_posts("media/post_photos/[FOLDER NAME]")'
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photoGraph.settings")

import django

django.setup()

from main.models import Post, UserProfile
from exif import Image
from django.core.files.images import ImageFile
import random


# Based on https://stackoverflow.com/a/73267185
def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def generate_posts(directory):
    test_user_profiles = UserProfile.objects.all()

    for filename in os.listdir(directory):
        try:
            print("\n" + filename)
            filename = directory + "/" + filename

            # Based on https://stackoverflow.com/a/73267185
            with open(filename, "rb") as src:
                img = Image(src)

            if img.has_exif:
                try:
                    coords = (
                        decimal_coords(img.gps_latitude, img.gps_latitude_ref),
                        decimal_coords(img.gps_longitude, img.gps_longitude_ref),
                    )

                    test_user_profile = random.choice(test_user_profiles)
                    Post.objects.create(
                        created_by=test_user_profile,
                        caption=filename.split("/")[-1],
                        photo=ImageFile(open(filename, "rb")),
                        latitude=coords[0],
                        longitude=coords[1],
                    )
                except AttributeError:
                    print("No Coordinates")

            else:
                print("The Image has no EXIF information")
        except Exception as e:
            print(e)


def main():
    print("Starting Peter's post population script...")
    generate_posts("media/post_photos/glasgow-test")
    print("Completed Peter's post population script.")


if __name__ == "__main__":
    main()
