from pytube import YouTube, Playlist
import os
import json

working_path = os.getcwd()

#---about the config file---#
#DOWNLOAD_PATH is where a folder containing your files will be created.
#FILE_QUALITY is the bitrate you want your file to be coded.

with open(f'{working_path}/VideoDownloader/app_config.json', 'r') as file:
    config = json.load(file)
    download_path_json = config['DOWNLOAD_PATH']
    file_quality_json = config['FILE_QUALITY']

download_path = f'{download_path_json}'
file_quality = f'{file_quality_json}'

file.close()

chooser = int(input('''

1 - Playlist de Vídeos
2 - Playlist de Músicas
3 - Vídeo
4 - Música

'''))

url = input('Link: ')


def SaveDir(name):
    path = os.path.join(download_path, name)

    os.mkdir(path)

    return path


def Pusher(path, filename, Download_path):
    for file in os.listdir(path):
        if file.endswith('.mp4'):

            os.remove(os.path.join(path, file))

        if file.endswith('.mp3'):

            os.rename(os.path.join(path, file), os.path.join(
                Download_path,
                    f'{filename}.mp3'))


def Puller(temp_path, download_path):
    for file in os.listdir(temp_path):
        os.remove(file)

    os.rmdir(download_path + 'temp')


def Converter(path, Download_path):
    storage = []

    for file in os.listdir(path):
        if file.endswith('.mp4'):

            archive_name = str(os.path.basename(file))
            storage.append(archive_name)

            file_name = os.path.join(path, file)
            new_name = os.path.join(path, f'{str(0)}.mp4')
            output_name = os.path.join(path, f'{str(0)}')

            os.rename(file_name, new_name)
            os.system(f'ffmpeg -i {new_name} -b:a {file_quality}K -vn {output_name}.mp3')

            Pusher(path, storage[0].split('.')[0], Download_path)


def ListVideos(link):
    playlist = Playlist(link)

    playlist_name = str(playlist.title)

    SaveDir('Videos')

    Download_Path = download_path + 'Videos'
    Final_Folder = download_path + f'{playlist_name}/'

    for video in playlist.videos:
        video.streams.get_highest_resolution().download(Download_Path)

    os.rename(Download_Path, Final_Folder)

    return print('Feito!')


def ListAudios(link):
    playlist = Playlist(link)

    playlist_name = str(playlist.title)

    SaveDir('Songs')

    Download_Path = download_path + 'Songs/'
    temp_path = os.path.join(Download_Path, 'temp')
    Final_Folder = download_path + f'{playlist_name}/'

    os.mkdir(temp_path)

    for video in playlist.videos:
        video.streams.get_audio_only().download(temp_path)
        Converter(temp_path, Download_Path)

    Puller(temp_path, Download_Path)

    os.rename(Download_Path, Final_Folder)

    return print('Feito!')


def Video(link):
    video = YouTube(link)

    video_name = str(video.title)

    SaveDir('Video')

    Download_Path = download_path + 'Video'
    Final_Folder = download_path + f'{video_name}/'
    
    video.streams.get_highest_resolution().download(Download_Path)

    os.rename(Download_Path, Final_Folder)

    return print('Feito!')


def Audio(link):
    audio = YouTube(link)

    audio_name = str(audio.title)

    SaveDir('Song')

    Download_Path = download_path + 'Song/'
    temp_path = os.path.join(Download_Path, 'temp')
    Final_Folder = download_path + f'{audio_name}/'

    os.mkdir(temp_path)

    audio.streams.get_audio_only().download(temp_path)

    Converter(temp_path, Download_Path)

    Puller(temp_path, Download_Path)

    os.rename(Download_Path, Final_Folder)

    return print('Feito!')


if chooser == 1:
    ListVideos(url)
elif chooser == 2:
    ListAudios(url)
elif chooser == 3:
    Video(url)
elif chooser == 4:
    Audio(url)
