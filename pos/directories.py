
ITEM_IMAGES_DIR = "items/"
ACCOUNT_DIR = "accounts/"

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'accounts/user_{0}/{1}'.format(instance.id, filename)