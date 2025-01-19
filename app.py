from filehandler import FileHandler
import configparser


def process_1(cfg):
    fh = FileHandler(cfg.get('DEFAULT', 'CARRIER_FILE_PATH'),
                     cfg.get('DEFAULT', 'DIRECTORY_TO_LOAD'),
                     cfg.get('DEFAULT', 'EXTENSIONS'))
    payl = fh.build_payload()
    encr_payload = fh.encrypter.encrypt(payl)
    fh.create_carrier_copy()
    fh.add_payload(encr_payload)


def process_2(cfg):
    fh = FileHandler(cfg.get('DEFAULT', 'CARRIER_FILE_WITH_PAYLOAD'))
    payl = fh.read_payload()
    decrypt_payl = fh.encrypter.decrypt(payl)
    fh.reconstruct_payload(decrypt_payl.decode('utf-8'),
                           cfg.get('DEFAULT', 'PROJECT_NAME'))


if __name__ == '__main__':
    config = configparser.RawConfigParser()
    config.read('config.ini')

    # process_1(config)
    process_2(config)
