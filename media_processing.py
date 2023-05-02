import os
import tempfile
import logging
import requests
from pydub import AudioSegment

logger = logging.getLogger(__name__)


class DownloadService:
    def __init__(self, chunk_size=8192, timeout=10):
        self.session = requests.Session()
        self.chunk_size = chunk_size
        self.timeout = timeout
        self.session.headers.update({
            "User-Agent": "mediamate/1.0"
        })

    def download_media_file(self, url):
        try:
            response = self.session.get(url, stream=True, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download the file from: {url}. Error: {e}")
            raise IOError(f"Failed to download the file. Error: {e}")

        with tempfile.NamedTemporaryFile(delete=False) as local_file:
            local_file_path = local_file.name
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                if chunk:
                    local_file.write(chunk)

        logger.info(f"File downloaded and saved locally at: {local_file_path}")
        return local_file_path


class AudioConverter:
    @staticmethod
    def create_temporary_mp3_file():
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3_file:
            return temp_mp3_file.name

    @staticmethod
    def load_and_convert_to_mp3(input_file_path, mp3_file_path):
        audio = AudioSegment.from_file(input_file_path)
        audio.export(mp3_file_path, format="mp3", codec="libmp3lame", parameters=["-q:a", "2"])

    @staticmethod
    def delete_file(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            logger.error(f"Failed to delete {file_path}: {str(e)}")

    @staticmethod
    def convert_to_mp3(input_file_path):
        mp3_file_path = AudioConverter.create_temporary_mp3_file()

        try:
            AudioConverter.load_and_convert_to_mp3(input_file_path, mp3_file_path)
        except Exception as e:
            logger.error(f"Failed to convert the input file to MP3: {str(e)}")
            AudioConverter.delete_file(mp3_file_path)
            raise e
        else:
            AudioConverter.delete_file(input_file_path)

        logger.info(f"Converted file: {os.path.basename(mp3_file_path)}")
        return mp3_file_path
