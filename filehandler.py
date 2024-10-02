import shutil
import os
from pathlib import Path
from encrypter import Encrypter


class FileHandler:
    def __init__(self, carrier_file, directory_to_encrypt=''):
        self.source_file = carrier_file
        self.copy_of_file = ''
        self.size_byte_len = 32
        self.dir_to_encrypt = directory_to_encrypt
        self.encrypter = Encrypter(b"5A44555D9D8BB7ADB345243351BABT56")

    def create_carrier_copy(self):
        dir_name = Path(self.source_file).parent.resolve()
        new_dir = dir_name / 'loaded'
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        self.copy_of_file = Path(new_dir) / Path(self.source_file).name
        shutil.copyfile(self.source_file, self.copy_of_file)

    def add_payload(self, payload: bytes):
        with open(self.copy_of_file, 'ab') as f:
            payload_len = len(payload)
            encoded_payload_length = str(payload_len).ljust(self.size_byte_len).encode('utf-8')
            f.write(payload)
            f.write(encoded_payload_length)

    def read_payload(self) -> bytes:
        with open(self.source_file, 'rb') as f:
            content = f.read()
            msg_len_b = content[-self.size_byte_len:]
            msg_len = int(msg_len_b.decode('utf-8'))
            payload = content[-(msg_len + self.size_byte_len):-self.size_byte_len]
        return payload

    def build_payload(self) -> bytes:
        data = ''
        for root, dirs, files in os.walk(self.dir_to_encrypt):
            for file in files:
                if file[-3:] == '.py':
                    file_full_name = os.path.join(root, file)
                    with open(file_full_name, 'rb') as f:
                        data += f'\n#  ------- START OF FILE {file_full_name} -------\n'
                        data += f.read().decode('utf8')
                        data += f'\n#  ------- END OF FILE {file_full_name} -------\n'

        binary_content = data.encode('utf-8')
        return binary_content

    @staticmethod
    def reconstruct_payload(payload: str, root_name: str):
        all_files = payload.split('START OF FILE ')
        f_start = all_files[0]
        for content in all_files[1:]:
            original_f_path = content.split(' ')[0]
            new_f_path = Path('assets').joinpath(root_name) / Path(original_f_path.split(root_name)[1]).name
            new_f_path.parent.mkdir(exist_ok=True, parents=True)
            new_f_path.write_text(f_start + content.replace("\r\n", "\n"))
        return


