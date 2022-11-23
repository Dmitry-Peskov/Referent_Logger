import os
import shutil
import zipfile

BASE_DIR = os.getcwd()
BASE_FOLDER = str()
LOGFILE_PATH = [fr'\log\Referent\Referent.log', fr'\CPCrypto.ini', fr'\Referent0.ini', fr'\referent.ini',
                fr'\Referent_Setup.ini', fr'\log\Referent\Reftransport.log', fr'\log\FormatCheck\FormatCheck.log',
                fr'\DocEngineError.log', fr'\dbconnection.ini', fr'\log\ManagedApp\WebModuleSystem.log']

def create_base_folder(input_login: str) -> None:
    '''Создать базовую папку для сбора log файлов'''
    folder = fr'{input_login} - log файлы'
    if not os.path.exists(folder):
        os.mkdir(folder)
        print(f'В "{BASE_DIR}" создана директория "{folder}"')
    else:
        print(f'"{folder}" уже существует в {BASE_DIR}')
    global BASE_FOLDER
    BASE_FOLDER = folder

def create_path_to_file(base_dir: str, input_login: str, logfile_path: list) -> list:
    '''Создать пути к log файлам'''
    lp = list()
    for log_path in logfile_path:
        lp.append(fr'{base_dir}{log_path}')
    lp.append(fr'{base_dir}\log\Referent\ref_crypto_{input_login}.log')
    lp.append(fr'{base_dir}\log\Referent\protocol_{input_login}.log')
    return lp

def copy_logfile(logfile_path: list, base_folder: str) -> None:
    '''Если файл существует -> копируем в директорию для сбора log файлов'''
    need_copy = len(logfile_path)
    copy = int()
    for log_path in logfile_path:
        log_name = log_path.split('\\')[-1]
        if os.path.exists(log_path) == True:
            try:
                shutil.copy(log_path, base_folder)
                copy += 1
                print(f'"{log_name}" скопирован в "{base_folder}"')
            except:
                print(f'Ошибка при копировании "{log_name}"')
        else: 
            print(f'"{log_name}" НЕ СУЩЕСТВУЕТ в "{log_path}"')
    print(f'\n-----Копирование завершено-----\nСкопировано {copy} из {need_copy} log файлов\n{"-"*31}\n')

def create_zip(base_folder: str) -> None:
    '''Создать zip архив и упаковать папку с log-ами в него'''
    archive = zipfile.ZipFile(f'{base_folder}.zip', mode='w')
    cnt_zip = int()
    for root, dirs, files in os.walk(base_folder): 
        for file in files:
            try:
                archive.write(os.path.join(root,file))
                cnt_zip += 1
                print(fr'"{file}" упакован в "{base_folder}.zip"')
            except:
                print(fr'Ошибка при упаковке "{file}" в "{base_folder}.zip"')
    archive.close()
    print(f'\n-----Упаковка завершена-----\nУпакован(но) {cnt_zip} файл(ов)\n{"-"*28}\n')

def delete_folder(base_dir: str, base_folder: str) -> None:
    '''Удаляет папку с собранными log файлами'''
    delete_folder = os.path.join(base_dir,base_folder)
    try:
        shutil.rmtree(delete_folder, ignore_errors=True)
        print(f'\n"{base_folder}" - папка удалена\n')
    except:
        print(f'\nНе удалось удалить папку "{base_folder}"\nПопробуйте осуществить удаление в ручную\n')

def main():
    '''Логика работы приложения'''
    login = str(input('Введите логин (системный ящик без домена): '))
    create_base_folder(login) # создаём папку для сбора log файлов
    log_pat = create_path_to_file(BASE_DIR, login, LOGFILE_PATH) # генерируем пути к log файлам
    copy_logfile(log_pat, BASE_FOLDER) # копируем log в папку для сбора
    create_zip(BASE_FOLDER) # упаковываем папку в zip архив
    delete_folder(BASE_DIR, BASE_FOLDER) # удаляем папку с собранными логами
    input(f'\nДля завершения работы нажмите "Enter" либо закройте консоль')

if __name__ == "__main__":
    main()
