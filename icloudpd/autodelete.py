"""
Delete any files found in "Recently Deleted"
"""
import os
import logging
from tzlocal import get_localzone
from icloudpd.logger import setup_logger
from icloudpd.paths import local_download_path


def autodelete_photos(icloud, folder_structure, directory):
    """
    Scans the "Recently Deleted" folder and deletes any matching files
    from the download directory.
    (I.e. If you delete a photo on your phone, it's also deleted on your computer.)
    """
    logger = setup_logger()
    logger.info("Deleting any files found in 'Recently Deleted'...")

    recently_deleted = icloud.photos.albums["Recently Deleted"]

    for media in recently_deleted:
        try:
            created_date = media.created.astimezone(get_localzone())
        except (ValueError, OSError):
            logger.set_tqdm_description(
                f"Could not convert media created date to local timezone {media.created}",
                logging.ERROR)
            created_date = media.created

        date_path = folder_structure.format(created_date)
        download_dir = os.path.join(directory, date_path)

        for size in [None, "original", "medium", "thumb"]:
            path = os.path.normpath(
                local_download_path(
                    media, size, download_dir))
            if os.path.exists(path):
                logger.info("Deleting %s!", path)
                os.remove(path)
