from __future__ import print_function
import argparse
import os
import datetime
import logging


class LogCleaner:

    logging.basicConfig(level=logging.DEBUG)

    def get_modification_time(self, file):
        try:
            modification_time = os.path.getmtime(file)
            file_mtime = datetime.datetime.fromtimestamp(modification_time)
            return file_mtime
        except FileNotFoundError:
            logging.warning("%s not found" % file)
            return datetime.datetime.fromtimestamp(0)

    def get_file_list(self, path):
        file_list = os.listdir(path)
        for file in file_list:
            logging.debug("Found %s" % file)
        return file_list

    def check_access_to_path(self, path):
        valid_access = os.access(r"%s" % path, os.R_OK | os.W_OK)
        return valid_access

    def list_files_older_than(self, hours_old, path):
        logging.debug("Entering %s" % "__method__")
        old_timestamp = datetime.timedelta(hours=hours_old)
        current_datetime = datetime.datetime.now()
        file_list = self.get_file_list(path)
        filtered_list = []
        for file in file_list:
            file_mtime = self.get_modification_time("%s%s%s" % (path, os.sep, file))
            if file_mtime == 0:
                continue
            elif file_mtime < (current_datetime - old_timestamp):
                logging.debug("%s: older than: %s hours" % (file, hours_old))
                filtered_list.append(file)
        logging.info("Found: %s files older than %s hours" % (len(filtered_list), hours_old))
        return filtered_list

    def list_paths_with_given_subfolder(self, base_path, subfolder=""):
        base_path_list = self.get_file_list(base_path)
        anteriores_path = []
        for folder in base_path_list:
            subfolder_path = "%s\\%s" % (folder, subfolder)
            if self.check_access_to_path(subfolder_path):
                anteriores_path.append(subfolder_path)
                logging.debug("Found: %s" % subfolder_path)
            else:
                logging.warning("%s is not accessible for R/W" % subfolder_path)
        logging.info("Found: %s folders with Anteriores subfolder" % len(anteriores_path))
        return anteriores_path

    def remove_listed_files(self, file_list):
        try:
            for file in file_list:
                os.remove(file)
                logging.info("Removed: %s" % file)
        except OSError as ose:
            affected_file = ose.filename
            message = ose.strerror
            logging.error("Cannot delete %s: %s" % (affected_file, message))


def __main__():
    parser = argparse.ArgumentParser(description='List/delete files last modified prior to a given number of hours ago')
    parser.add_argument('path', help='base path where files will be searched')
    parser.add_argument('hours_old', help='Hours past since last modification time', type=int)
    parser.add_argument('--delete', help="Set if you want to delete listed files", type=bool, default=False)
    parser.add_argument('--subfolder', help='SubFolder inside each folder in the path where files will be searched')
    args = parser.parse_args()

    file_expiration = args.hours_old
    path = args.path
    subfolder = args.subfolder
    delete = args.delete

    files = []
    lg = LogCleaner()

    if subfolder != None:
        anteriores_path = lg.list_paths_with_given_subfolder(path, subfolder)
        for anterior in anteriores_path:
            files.append(lg.list_files_older_than(file_expiration, anterior))
    else:
        files.append(lg.list_files_older_than(file_expiration, path))

    if delete:
        logging.info("Delete files is selected")
        lg.remove_listed_files(files)
    else:
        logging.info("No files will be deleted")

if __name__ == "__main__":
    __main__()
