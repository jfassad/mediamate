import os
import tempfile
import logging
import requests
import openai
from pydub import AudioSegment
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)


def _download_media_file(url):
    session = requests.Session()
    chunk_size = 8192
    timeout = 10
    session.headers.update({
        "User-Agent": "mediamate/1.0"
    })

    try:
        response = session.get(url, stream=True, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download the file from: {url}. Error: {e}")
        raise IOError(f"Failed to download the file. Error: {e}")

    with tempfile.NamedTemporaryFile(delete=False) as local_file:
        local_file_path = local_file.name
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                local_file.write(chunk)

    logger.debug(f"File downloaded and saved locally at: {local_file_path}")
    return local_file_path


def _create_temporary_mp3_file():
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3_file:
        return temp_mp3_file.name


def _load_and_convert_to_mp3(input_file_path, mp3_file_path):
    audio = AudioSegment.from_file(input_file_path)
    audio.export(mp3_file_path, format="mp3", codec="libmp3lame", parameters=["-q:a", "2"])


def _delete_file(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        logger.error(f"Failed to delete {file_path}: {str(e)}")


def _convert_to_mp3(input_file_path):
    mp3_file_path = _create_temporary_mp3_file()

    try:
        _load_and_convert_to_mp3(input_file_path, mp3_file_path)
    except Exception as e:
        logger.error(f"Failed to convert the input file to MP3: {str(e)}")
        _delete_file(mp3_file_path)
        raise e
    else:
        _delete_file(input_file_path)

    logger.debug(f"Converted file: {os.path.basename(mp3_file_path)}")
    return mp3_file_path


def transcribe_audio(url):
    local_file_path = _download_media_file(url)
    logger.debug(f"Downloaded file path: {local_file_path}")
    output_mp3_file = _convert_to_mp3(local_file_path)
    logger.debug(f"Output MP3 file: {output_mp3_file}")

    with open(output_mp3_file, 'rb') as file:
        resp = openai.Audio.transcribe(
            api_key=OPENAI_API_KEY,
            file=file,
            model='whisper-1',
            response_format='text'
        )
        _delete_file(output_mp3_file)
    return resp
