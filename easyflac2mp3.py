import fileinput
import os
import shutil


def flac2mp3(file, filename):
    cmdfile = '"' + file + '"'
    tag = file + ".tag"
    cmdtag = '"' + tag + '"'
    os.system("metaflac --no-utf8-convert --export-tags-to=" + cmdtag + " " + cmdfile)
    for tagline in fileinput.input(tag, inplace=True):
            print(tagline.replace("TITLE=", "--tt "), end='')
            print(tagline.replace("Title=", "--tt "), end='')
            print(tagline.replace("ARTIST=", "--ta "), end='')
            print(tagline.replace("Artist=", "--ta "), end='')
            print(tagline.replace("ALBUM=", "--tl "), end='')
            print(tagline.replace("Album=", "--tl "), end='')
            print(tagline.replace("TRACKNUMBER=", "--tn "), end='')
            print(tagline.replace("GENRE=", "--tg "), end='')
            print(tagline.replace("DATE=", "--ty "), end='')

    with open(tag, "r+") as tagfix:
        lines = tagfix.readlines()

        # Rewind and truncate
        tagfix.seek(0)
        tagfix.truncate()

        for line in lines:
            line = line[0:5] + '"' + line[5:-1] + '" '
            if line.startswith("--"):
                tagfix.write(line)

    filer = open(tag, 'r')
    args = filer.read()
    filer.close()
    mp3 = '"' + file[0:-5] + ".mp3" + '"'
    osmp3 = file[0:-5] + ".mp3"
    mp3file = filename[0:-5] + ".mp3"
    wav = '"' + file[0:-5] + ".wav" + '"'
    delwav = file[0:-5] + ".wav"
    os.system("flac -d -F " + cmdfile)
    os.system("lame " + br + " " + args + " " + wav + " " + mp3)
    os.remove(delwav)
    os.remove(tag)
    try:
        outdir
    except NameError:
        pass
    else:
        shutil.copy2(osmp3, outdir + mp3file)
        os.remove(osmp3)

def inputflac():
    print('Are you converting a single "file" or a "folder"? (Enter one of the two.)')
    source = input()
    if source in ('file', 'folder'):
        if source == "file":
            print('Enter the filename.')
            file = input()
            filename = os.path.basename(file)
            outputdir()
            flac2mp3(file, filename)
        elif source == "folder":
            print('Enter the folder name.')
            folder = input()
            outputdir()

            for file in os.listdir(folder):
                filename = file
                file = os.path.join(folder, file)
                if file.endswith(".flac"):
                    flac2mp3(file, filename)
    else:
        print('Please enter "file" or "folder".')

def outputdir():
    global outdir
    print('Do you want to save the mp3(s) into the same folder or a different location? (Enter "same" or "different".')
    output = input()
    if output == "same":
        return
    else:
        print('Enter the directory you wish to save the MP3s into.')
        directory = input()
        outdir = os.path.join(directory, '')
        try:
            os.makedirs(outdir)
        except OSError:
            pass


print('Enter "0"-"9" for a VBR or "b[bitrate]" (e.g. b320) for a CBR')
bitrate = input()

if bitrate[0] == "b":
    br = '-' + str(bitrate)
else:
    if int(bitrate) < 10 and int(bitrate) > -1:
        br = '-V' + str(bitrate)
    else:
        "Please try again."

inputflac()
