#-------------------------------------------------------------------------------
# Name:         pydedup
# Purpose:      Works on deduplication of files.
#               
#
# Author:       Matthieu Viguier 
#
# Created:      04/10/2022
# Copyright:    (c) Matthieu 2022
# Licence:      GNU GPLV3
# Usage :       pydedup dir1 dir2
# Tips :        dir1 : source / dir2 : cible
#-------------------------------------------------------------------------------
try :
    import glob
    import os
    import sqlite3
    import pathlib
    import hashlib
    import shutil
    from PIL import Image
    import logging
    from tqdm import tqdm
    import fnmatch
    import datetime
    import sys


### TIPS
## How to log
# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')

except :
    print("Erreur d'import des modules")
    exit()

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        logging.warning(e)
    finally:
        if conn:
            return conn

def tprint(message):
    return str(str((datetime.datetime.now())) + " : " + message)

def show(message):
    print(tprint(message))
    logging.warning(tprint(message))

def noshow(message):
    logging.warning(tprint(message))

def alliter(p):
    yield p
    for sub in p.iterdir():
        if sub.is_dir():
            yield from alliter(sub)
        else:
            yield sub

def type(ext):
    images=['jpg','png']
    videos=['avi']
    for i in images:
        if i in ext:
            return "photo"
    for j in videos:
        if j in ext:
            return "video" 
    return "unknown"

def main():
        logging.basicConfig(filename='pyfidup.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        show("pyfidup -- démarré")
        conn=create_connection(r"E:\Photos.db")
        show("pyfidup -- Listing en cours")
        cpt = sum([len(files) for r, d, files in os.walk("E:\gdrive_m.viguier\Photos")])
        nb=cpt
        show("pyfidup -- Listing : "+str(nb))
        g = alliter(pathlib.Path("E:\gdrive_m.viguier\Photos\\"))
        with tqdm(total=nb) as pbar:
            for a in g :
                if a.is_file():
                    fext=str(a).split(".")[-1]
                    if 'db' not in fext:
                        try :
                            pbar.update(1)
                            f_size = os.stat(a).st_size
                            im=Image.open(a)
                            x=str(im.width)
                            y=str(im.height)
                            im.close()
                            fname=str(a).split("\\")[-1]
                            fext=str(a).split(".")[-1]
                            a_file = open(a, "rb")
                            content = a_file.read()
                            a_file.close()
                            md5_hash_content = hashlib.md5()
                            md5_hash_content.update(content)
                            digest_file = md5_hash_content.hexdigest()
                            md5_hash_name=hashlib.md5()
                            md5_hash_name.update(fname.encode())
                            digest_filename=md5_hash_name.hexdigest()
                            #logging.warning(digest_file)
                            #sql="SELECT file_path from hash_set WHERE file_md5='"+str(digest_file)+"'"
                            sql="INSERT INTO hash_set (photo_x, photo_y, file_type, file_ext, file_size, filename, file_full_md5, file_path, filename_md5) VALUES ('"+x+"','"+y+"','"+str(type(fext))+"','"+str(fext)+"','"+str(f_size)+"','"+str(fname)+"','"+str(digest_file)+"','"+str(a)+"','"+str(digest_filename)+"')"
                            #logging.warning(sql)
                            cur = conn.cursor()
                            cur.execute(sql)
                            conn.commit()
                            # res=cur.fetchall()
                            # if res:
                            #     logging.warning(str(a)+" --- collision sur --- DB["+str(res[0][0])+"]")
                            #     a_file.close()
                            #     shutil.move(str(a), "D:\doublons\\"+fname)
                        except Exception as e:
                            err = str(e)
                            match err:
                                case "UNIQUE constraint failed: hash_set.file_full_md5":
                                    noshow(err+ " --- on --- " + str(a))
                                    shutil.move(a, "D:\\doublons2\\"+fname)
                                case "cannot identify image file":
                                    noshow(err+ " --- on --- " + str(a))
                                    shutil.move(a, "D:\\no_img\\"+fname)
                                case _ :
                                    show(show(err))
                                    exit() 
            show("pyfidup -- terminé")

# def main2():
#     if len(sys.argv) > 1:
#         if sys.argv[1] =="verify":
#             exit()
#         if sys.argv[1] =="full_run":
#             logging.basicConfig(filename='pyfidup.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
#             show("pyfidup -- démarré")
#             conn=create_connection(r"E:\Photos.db")
#             show("pyfidup -- Listing en cours")
#             cpt = sum([len(files) for r, d, files in os.walk("E:\gdrive_m.viguier\Photos")])
#             nb=cpt
#             show("pyfidup -- Listing : "+str(nb))
#             g = alliter(pathlib.Path("E:\gdrive_m.viguier\Photos\\"))
#             with tqdm(total=nb) as pbar:
#                 for a in g :
#                     if a.is_file():
#                         fext=str(a).split(".")[-1]
#                         if 'db' not in fext:
#                             try :
#                                 pbar.update(1)
#                                 f_size = os.stat(a).st_size
#                                 im=Image.open(a)
#                                 x=str(im.width)
#                                 y=str(im.height)
#                                 im.close()
#                                 fname=str(a).split("\\")[-1]
#                                 fext=str(a).split(".")[-1]
#                                 a_file = open(a, "rb")
#                                 content = a_file.read()
#                                 a_file.close()
#                                 md5_hash_content = hashlib.md5()
#                                 md5_hash_content.update(content)
#                                 digest_file = md5_hash_content.hexdigest()
#                                 md5_hash_name=hashlib.md5()
#                                 md5_hash_name.update(fname.encode())
#                                 digest_filename=md5_hash_name.hexdigest()
#                                 #logging.warning(digest_file)
#                                 #sql="SELECT file_path from hash_set WHERE file_md5='"+str(digest_file)+"'"
#                                 sql="INSERT INTO hash_set (photo_x, photo_y, file_type, file_ext, file_size, filename, file_full_md5, file_path, filename_md5) VALUES ('"+x+"','"+y+"','"+str(type(fext))+"','"+str(fext)+"','"+str(f_size)+"','"+str(fname)+"','"+str(digest_file)+"','"+str(a)+"','"+str(digest_filename)+"','"+str("")+"')"
#                                 #logging.warning(sql)
#                                 cur = conn.cursor()
#                                 cur.execute(sql)
#                                 conn.commit()
#                                 # res=cur.fetchall()
#                                 # if res:
#                                 #     logging.warning(str(a)+" --- collision sur --- DB["+str(res[0][0])+"]")
#                                 #     a_file.close()
#                                 #     shutil.move(str(a), "D:\doublons\\"+fname)
#                             except Exception as e:
#                                 if str("UNIQUE constraint failed: hash_set.file_full_md5") in str(e):
#                                     noshow(str(e)+ " --- on --- " + str(a))
#                                     shutil.move(a, "D:\\doublons2\\"+fname)
#                                 if str("cannot identify image file") in str(e):
#                                     noshow(str(e)+ " --- on --- " + str(a))
#                                     shutil.move(a, "D:\\no_img\\"+fname)
                            
                    
#             show("pyfidup -- terminé")
#         else:
#             exit()
#     else:
#         show("pyfidup -- nead arg !")
#         exit()

if __name__ == '__main__':
    main()
